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
def start_server():
    server=RestServer()
    server.register_route(urlpatterns=["/"],verbs=["GET"]);
    server.serve_forever()

def initialize(*args):
    client = RestClient(url="http://localhost:3333")
    client.agent.request(*args)
    return client

class RestServerLiveTests(unittest.TestCase,BaseUnitTest):
    def __init__(self,testmethod=None):
        if testmethod:
            super(RestServerLiveTests,self).__init__(testmethod)

    def test_get(self):
        client = initialize("GET","/")
        response = client.agent.getresponse()
        self.assertEquals(response.status,200)

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
    start_server()
