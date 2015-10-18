#!/usr/bin/env python
import time # might be used for shutdown
import re
import socket
import signal
import sys
import urlparse

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from multiprocessing import Process, Event, Semaphore, Value, cpu_count
from SocketServer import BaseServer # for shutdown
from threading import Thread
#sys.path.append('../../../oldpeculier')
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
        self._thread_n = getattr(self, '_thread_n', 64)
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
        for p in self._processes:
            print "shutting down process %s" %(p.pid)
            p.terminate()
        exit(0)

def default_handler(request):
    message = "\nThis is the default handler. It echo's what you send.\n\n"
    message += "REQUEST HEADERS\n"
    for header in request.headers.keys():
        message += " > {0}: {1}\n".format(header,request.headers.get(header))
    message += "\nREQUEST PARAMETERS\n" 
    parsed_url = urlparse.urlparse(request.path)
    if  parsed_url.query:
        params = urlparse.parse_qs(parsed_url.query)
        for param in params.keys():
            value=params.get(param)
            if isinstance(value,list):
                for v in value:
                    message += " > {0}: {1}\n".format(param,v)
            else:
                message += " > {0}: {1}\n".format(param,params.get(param))
    message += "\nREQUEST BODY\n" 
    if request.headers.has_key('Content-Length'):
        contentlength = int(request.headers.get('Content-Length'))
        body = request.rfile.read(contentlength)
        message += body+"\n"
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
        

class RestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        match_length=0
        route_handler=None
        for route in self.server.routes["GET"]:
            for url in route["urls"]:
                match = re.compile("("+url+")").match(self.path)
                if hasattr(match,"groups"):
                    matched_group = match.group()
                    if match_length < matched_group:
                        match_length= len(matched_group)
                        route_handler = route["handler"]
        if route_handler:
            route_handler(self)

    def do_POST(self):
        match_length=0
        route_handler=None
        for route in self.server.routes["GET"]:
            for url in route["urls"]:
                match = re.compile("("+url+")").match(self.path)
                if hasattr(match,"groups"):
                    matched_group = match.group()
                    if match_length < matched_group:
                        match_length= len(matched_group)
                        route_handler = route["handler"]
        if route_handler:
            route_handler(self)

