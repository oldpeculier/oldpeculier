#!/usr/bin/env python
import atexit
import json
import os
import requests
import shutil
import signal
import sys
import tempfile
import time
import unittest
from oldpeculier.rest.server import RestServer, RestHandler
from oldpeculier.tests.unit.base import BaseUnitTest
import threading

thread = None
parent_thread = None
port = 3332
address =  "localhost"

def exit_handler():
    if dirpath:
        shutil.rmtree(dirpath)

def start_server(loglevel=None):
    global server, dirpath
    dirpath = tempfile.mkdtemp()
    server=RestServer(logger_level=loglevel, bind_address=address, port=port,
        logger_location=dirpath+"/"+"live_rest_tests.log")
    server.register_route(urlpatterns=["/"],verbs=["GET","PUT"]);
    server.register_route(urlpatterns=["/post"],verbs=["POST"]);
    atexit.register(exit_handler)
    server.serve_forever()

class RestServerLiveTests(unittest.TestCase,BaseUnitTest):
    def __init__(self,testmethod=None, loglevel=None):
        self.base_url = "http://" + address + ":" + str(port)
        if testmethod:
            super(RestServerLiveTests,self).__init__(testmethod)

    def test_get_with_default_handler(self):
        response = requests.get(self.base_url)
        self.assertEquals(response.status_code,200)
        body = response.text
        self.assertRegexpMatches(body,".*GET.*")
        self.assertRegexpMatches(body,".*" + address + ":" + str(port) + ".*")
        self.assertRegexpMatches(body,".*REQUEST HEADERS.*")
        self.assertRegexpMatches(body,".*REQUEST BODY.*")
        self.assertRegexpMatches(body,".*REQUEST PARAMETERS.*")

    def test_post_with_default_handler(self):
        headers = {
            "content-type":"application/x-www-form-urlencoded"
        }
        data = {
            "token":"abc"
        }
        response = requests.post(self.base_url+"/post?token=123", headers=headers,
            data=data)    
        self.assertEquals(response.status_code,200)
        body = response.text
        self.assertRegexpMatches(body,".*POST.*\/post")
        self.assertRegexpMatches(body,".*" + address + ":" + str(port) + ".*")
        self.assertRegexpMatches(body,".*content-type.*application.*www-form.*")
        self.assertRegexpMatches(body,".*REQUEST HEADERS.*")
        self.assertRegexpMatches(body,".*REQUEST BODY.*")
        self.assertRegexpMatches(body,".*34b5239544b531f3b3c430df9a02363c.*")
        self.assertRegexpMatches(body,".*REQUEST PARAMETERS.*")
        self.assertRegexpMatches(body,".*token: 123.*")

    def test_put_with_default_handler(self):
        headers = {
            "content-type":"application/json"
        }
        data = {
            "token":"abc"
        }
        response = requests.put(self.base_url+"?token=123", headers=headers,
            data=json.dumps(data,separators=(',',':')))    
        self.assertEquals(response.status_code,200)
        body = response.text
        self.assertRegexpMatches(body,".*PUT.*")
        self.assertRegexpMatches(body,".*" + address + ":" + str(port) + ".*")
        self.assertRegexpMatches(body,".*content-type.*application.*json.*")
        self.assertRegexpMatches(body,".*REQUEST HEADERS.*")
        self.assertRegexpMatches(body,".*REQUEST BODY.*")
        self.assertRegexpMatches(body,".*6fe576639319fefd7b6785c11b06a694.*")
        self.assertRegexpMatches(body,".*REQUEST PARAMETERS.*")
        self.assertRegexpMatches(body,".*token: 123.*")

    #def test_post_multi_part(self):
#>>> from cgi import parse_multipart
#>>> d=parse_multipart(open("/tmp/junk"),{'boundary':'86cf9e25db6444c0a70f09b3ba63e57b'})
    #    files = [('name1', open("./restserver.py","rb")),('name2',open("../../common.py"))]
    #    response = requests.put(self.base_url+"?token=123", files=files)
    #    self.assertEquals(response.status_code,200)
    #    body = response.text
    #    print body

    def test_post_binary_file(self):
        with open("./random.bits","rb") as f:
            response = requests.put(self.base_url+"?token=123", data=f)
        self.assertEquals(response.status_code,200)
        body = response.text
        self.assertRegexpMatches(body,".*PUT.*")
        self.assertRegexpMatches(body,".*" + address + ":" + str(port) + ".*")
        self.assertRegexpMatches(body,".*application.*stream.*")
        self.assertRegexpMatches(body,".*REQUEST HEADERS.*")
        self.assertRegexpMatches(body,".*REQUEST BODY.*")
        self.assertRegexpMatches(body,".*17e56442d3da89ba2f46dd43781864e9.*")
        self.assertRegexpMatches(body,".*REQUEST PARAMETERS.*")
        self.assertRegexpMatches(body,".*token: 123.*")

    def test_rest_server_logging(self):
        self.assertTrue(os.path.exists(dirpath))

def start_live_tests():
    # give the server time to start
    tries=10
    attempts=0
    time.sleep(0.1)
    while not thread.is_alive():
        time.sleep(1)
        attempts+=1
        if attempts>tries:
            break;
    RestServerLiveTests().main(sys.argv[1:])
    os.kill(os.getpid(),signal.SIGINT);

if __name__ == '__main__':
    parent_thread = threading.current_thread()
    thread = threading.Thread(target=start_live_tests, args=(), kwargs={})
    thread.start()
    start_server(RestServerLiveTests().get_log_level(sys.argv))
