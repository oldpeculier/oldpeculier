#!/usr/bin/env python
import json
import magic
import re
import socket
import signal
import sys
import time # might be used for shutdown
import urlparse
import hashlib

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from multiprocessing import Process, Event, Semaphore, Value, cpu_count
from SocketServer import BaseServer # for shutdown
from threading import Thread
from oldpeculier.common import Common

# Credit to Muayyad Alsadi:
# https://github.com/muayyad-alsadi/python-PooledProcessMixIn
class PooledProcessMixIn:
    def _handle_request_noblock(self):
        self._event.clear()
        self._semaphore.release()
        self._event.wait()

    def _real_handle_request_noblock(self):
        try:
            # next line will do self.socket.accept()
            request, client_address = self.get_request()
        except socket.error:
            self._event.set()
            return
        self._event.set()
        if self.verify_request(request, client_address):
            try:
                self.process_request(request, client_address)
                self.shutdown_request(request)
            except:
                self.handle_error(request, client_address)
                self.shutdown_request(request)


    def __init__(self):
        self._process_n = getattr(self, '_process_n', max(2, cpu_count()))
        self._thread_n = getattr(self, '_thread_n', 63)
        self._keep_running = Value('i', 1)
        self._event = Event()
        self._semaphore = Semaphore(1)
        self._semaphore.acquire()
        self._maintain_pool()
    
    def _maintain_pool(self):
        self._processes = []
        for i in range(self._process_n):
            t = Process(target=self._process_loop)
            t.start()
            self._processes.append(t)

    def _process_loop(self):
        threads = []
        for i in range(self._thread_n):
            t = Thread(target=self._thread_loop)
            t.setDaemon(0)
            t.start()
            threads.append(t)
        # we don't need this because they are non-daemon threads
        # but this did not work for me
        # FIXME: replace this with event
        #self._shutdown_event.wait()
        for t in threads: t.join()

    def _thread_loop(self):
        while(self._keep_running.value):
            self._semaphore.acquire() # wait for resource
            self._real_handle_request_noblock()

    def shutdown(self,signal=None,frame=None):
        print ""
        for p in self._processes:
            self.logger.info("shutting down process %s" %(p.pid))
            p.terminate()
        exit(0)

def default_handler(request):
    qparams={} # params provided by url
    bparams={} # params provided by the body
    params={} # combined results
    #print dir(request)
    message = "\nThis is the default handler. It echo's what you send.\n\n"
    message += "{0} {1} {2}\nREQUEST HEADERS\n".format(
        request.method,request.path,request.protocol_version)
    for header in request.headers.keys():
        message += " > {0}: {1}\n".format(header,request.headers.get(header))

    parsed_url = urlparse.urlparse(request.path)
    if  parsed_url.query:
        qparams = request.get_form_params(parsed_url.query)

    message += "REQUEST BODY\n" 
    if request.headers.has_key('Content-Length'):
        contentlength = int(request.headers.get('Content-Length'))
        sample_size = 1024
        bytes_received = 0
        sig = hashlib.md5()
        body = None
        body_sample = None
        contenttype = request.headers.get('Content-Type')

        while True:
            body = request.rfile.read(min(sample_size,contentlength-bytes_received))
            if not body:
                break
            if not body_sample:
                body_sample = body
            if not contenttype:
                contenttype = magic.from_buffer(body,mime=True)
            bytes_received += min(len(body),request.rfile.default_bufsize)
            sig.update(body)

        message += " > ({0}) bytes of {2} data received.  MD5={1}\n".format(
            bytes_received,sig.hexdigest(),contenttype)
        #body = request.rfile.read(min(contentlength,sample_size))
        #contenttype = request.headers.get('Content-Type')
        #if contenttype == None:
        #    contenttype = magic.from_buffer(body,mime=True)
        if contenttype != "application/octet-stream":
            try:
                bparams = json.loads(body_sample)
                body_sample = json.dumps(bparams, indent=2, 
                    separators=(',',': '))
            except ValueError, e:
                bparams = request.get_form_params(body_sample)
                pass
            message += body_sample+"\n" # Just give back the first 1k
        #else:
        #    bytes_received = len(body)
        #    sig = hashlib.md5()
        #    sig.update(body)
        #    while True:
        #        body = request.rfile.read(min(sample_size,contentlength-bytes_received))
        #        if not body:
        #            break
        #        sig.update(body)
        #        bytes_received += min(len(body),request.rfile.default_bufsize)
        #    message += " > ({0}) bytes of binary data received.  MD5={1}\n".format(
        #        bytes_received,sig.hexdigest())
    params = qparams
    for key,value in bparams.iteritems():
        if not params.has_key(key):
             params[key]=value
        else:
            if not isinstance(params[key],list):
                params[key]=[params[key]]
            params[key].append(value)
    #params = dict(qparams.items() + bparams.items())
    message += "REQUEST PARAMETERS\n" 
    for key, param in params.items():
        if isinstance(param,list):
            for p in param:
                message += " > {0}: {1}\n".format(key,p)
        else:
            message += " > {0}: {1}\n".format(key,param)
    request.server.logger.debug("START: Writing output to %s" %request.client_address[0])
    request.server.logger.debug("\n%s" %message)
    request.server.logger.debug("DONE: Writing output to %s" %request.client_address[0])
    request.send_response(200)
    request.send_header("Content-Length",len(message))
    request.end_headers()
    request.wfile.write(message)

class RestServer(PooledProcessMixIn, HTTPServer, Common):
    routes={}
    def __init__(self, **kwargs):
        Common.__init__(self, **kwargs)

    def register_route(self, urlpatterns, verbs, handler=default_handler):
        for verb in verbs:
            if verb not in self.routes:
                self.routes[verb]=[]
            self.routes[verb].append({'urls':urlpatterns,'handler':handler})

    def serve_forever(self):
        HTTPServer.__init__(self, ('localhost',3333), RestHandler)
        PooledProcessMixIn.__init__(self)
        signal.signal(signal.SIGINT,self.shutdown)
        return super(RestServer,self).serve_forever()

    def shutdown_server(self):
        self.shutdown()

class RestHandler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'
    def get_form_params(self,content):
        params = urlparse.parse_qs(content)
        for key, param in params.items():
            if len(param) == 1:
                params[key]=param[0]
        return params

    def log_message(self, frmt, *args):
        #print self.server.logger.getEffectiveLevel()
        if self.server.logger.getEffectiveLevel() <= 20:
            self.server.logger.info("%s %s" %(self.client_address[0],frmt%args))

    def authorization_required(self,message="Authorization Required\n"):
        self.send(code=401, message=message)

    def not_authorized(self,message="Forbidden\n"):
        self.send(code=403, message=message)

    def not_found(self,message="Not Found\n"):
        self.send(code=404, message=message)

    def method_not_allowed(self,message="Method Not Allowed\n"):
        self.send(code=405, message=message)
    
    def conflict(self,message="Conflict\n"):
        self.send(code=409, message=message)

    def unsupported_media_type(self,message="Unsupported Media Type\n"):
        self.send(code=415, message=message)

    def send(self,code,message):
        self.send_response(code)
        self.send_header("Content-Length",len(message))
        self.end_headers()
        self.wfile.write(message)

    def _run_route(self,method):
        match_length=0
        route_handler=None
        try:
            for route in self.server.routes[method]:
                for url in route["urls"]:
                    match = re.compile("("+url+")($|\?|;)").match(self.path)
                    if hasattr(match,"groups"):
                        matched_group = match.group()
                        if match_length < matched_group:
                            match_length= len(matched_group)
                            route_handler = route["handler"]
            if route_handler:
                route_handler(self)
            else:
                self.not_found()
        except KeyError, e:
            self.not_found()

    def do_GET(self):
        self.method="GET"
        self._run_route(self.method)

    def do_POST(self):
        self.method="POST"
        self._run_route(self.method)

    def do_PUT(self):
        self.method="PUT"
        self._run_route(self.method)

    def do_DELETE(self):
        self.method="DELETE"
        self._run_route(self.method)

    def do_HEAD(self):
        self.method="HEAD"
        self._run_route(self.method)
