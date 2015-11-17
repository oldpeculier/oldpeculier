#!/usr/bin/env python
import os
import sys
import time
import unittest
import signal
from oldpeculier.rest.server import RestServer, RestHandler
from oldpeculier.rest.client import RestClient
from oldpeculier.tests.unit.base import BaseUnitTest
import threading

thread=None
parent_thread=None
def start_server(loglevel=None):
    server=RestServer(logger_level=loglevel)
    server.register_route(urlpatterns=["/"],verbs=["GET"]);
    server.serve_forever()

class RestServerLiveTests(unittest.TestCase,BaseUnitTest):
    def __init__(self,testmethod=None, loglevel=None):
        if testmethod:
            self.client = RestClient(url="http://localhost:3333",logger_level=loglevel)
            super(RestServerLiveTests,self).__init__(testmethod)

    def test_get_with_default_handler(self):
        self.client.agent.request("GET","/")
        response = self.client.agent.getresponse()
        self.assertEquals(response.status,200)
        body = response.read()
        self.assertRegexpMatches(body,".*localhost:3333.*")
        self.assertRegexpMatches(body,".*REQUEST HEADERS.*")
        self.assertRegexpMatches(body,".*REQUEST BODY.*")
        self.assertRegexpMatches(body,".*REQUEST PARAMETERS.*")

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