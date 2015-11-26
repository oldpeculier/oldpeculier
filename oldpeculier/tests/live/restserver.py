#!/usr/bin/env python
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
    server.register_route(urlpatterns=["/"],verbs=["GET"]);
    server.register_route(urlpatterns=["/"],verbs=["POST"]);
    server.serve_forever()

class RestServerLiveTests(unittest.TestCase,BaseUnitTest):
    def __init__(self,testmethod=None, loglevel=None):
        if testmethod:
            super(RestServerLiveTests,self).__init__(testmethod)

    def test_get_with_default_handler(self):
        response = requests.get("http://localhost:3333")
        self.assertEquals(response.status_code,200)
        body = response.text
        self.assertRegexpMatches(body,".*localhost:3333.*")
        self.assertRegexpMatches(body,".*REQUEST HEADERS.*")
        self.assertRegexpMatches(body,".*REQUEST BODY.*")
        self.assertRegexpMatches(body,".*REQUEST PARAMETERS.*")

    #def test_post_with_default_handler(self):
    #    headers = {
    #        "content-type":"application/x-www-form-urlencoded"
    #    }
    #    response = self.client.request("POST","/","{\"token\":\"abc\"}",headers)
    #    #response = self.client.agent.getresponse()
    #    self.assertEquals(response.status,200)
    #    body = response.read()
    #    print body
    #    self.assertRegexpMatches(body,".*localhost:3333.*")
    #    self.assertRegexpMatches(body,".*REQUEST HEADERS.*")
    #    self.assertRegexpMatches(body,".*REQUEST BODY.*")
    #    self.assertRegexpMatches(body,".*REQUEST PARAMETERS.*")

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
