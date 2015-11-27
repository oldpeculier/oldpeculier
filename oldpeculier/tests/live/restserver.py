#!/usr/bin/env python
import json
import os
import requests
import signal
import sys
import time
import unittest
from oldpeculier.rest.server import RestServer, RestHandler
from oldpeculier.tests.unit.base import BaseUnitTest
import threading

thread=None
parent_thread=None
def start_server(loglevel=None):
    server=RestServer(logger_level=loglevel)
    server.register_route(urlpatterns=["/"],verbs=["GET","PUT"]);
    server.register_route(urlpatterns=["/post"],verbs=["POST"]);
    server.serve_forever()

class RestServerLiveTests(unittest.TestCase,BaseUnitTest):
    def __init__(self,testmethod=None, loglevel=None):
        self.base_url = "http://localhost:3333"
        if testmethod:
            super(RestServerLiveTests,self).__init__(testmethod)

    def test_get_with_default_handler(self):
        response = requests.get(self.base_url)
        self.assertEquals(response.status_code,200)
        body = response.text
        self.assertRegexpMatches(body,".*GET.*")
        self.assertRegexpMatches(body,".*localhost:3333.*")
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
        self.assertRegexpMatches(body,".*localhost:3333.*")
        self.assertRegexpMatches(body,".*content-type.*application.*www-form.*")
        self.assertRegexpMatches(body,".*token:.*123.*")
        self.assertRegexpMatches(body,".*token:.*abc.*")
        self.assertRegexpMatches(body,".*REQUEST HEADERS.*")
        self.assertRegexpMatches(body,".*REQUEST BODY.*")
        self.assertRegexpMatches(body,".*REQUEST PARAMETERS.*")

    def test_put_with_default_handler(self):
        headers = {
            "content-type":"application/json"
        }
        data = {
            "token":"abc"
        }
        response = requests.put(self.base_url+"?token=123", headers=headers,
            data=json.dumps(data))    
        self.assertEquals(response.status_code,200)
        body = response.text
        self.assertRegexpMatches(body,".*PUT.*")
        self.assertRegexpMatches(body,".*localhost:3333.*")
        self.assertRegexpMatches(body,".*content-type.*application.*json.*")
        self.assertRegexpMatches(body,".*token:.*123.*")
        self.assertRegexpMatches(body,".*token:.*abc.*")
        self.assertRegexpMatches(body,".*REQUEST HEADERS.*")
        self.assertRegexpMatches(body,".*REQUEST BODY.*")
        self.assertRegexpMatches(body,".*REQUEST PARAMETERS.*")

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
        print body

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
