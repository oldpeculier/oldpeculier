#!/bin/env python
import sys
sys.path.append('../../../../oldpeculier/')
import unittest
from oldpeculier.rest.server import RestServer
from oldpeculier.tests.unit.base import BaseUnitTest
from httplib import HTTPConnection, HTTPSConnection

def initialize(**kwargs):
    return RestServer(**kwargs)

class RestServerTests(unittest.TestCase,BaseUnitTest):
    def __init__(self,testmethod=None):
        if testmethod:
            super(RestServerTests,self).__init__(testmethod)
    
    def test_initialize(self):
        try:
            initialize()
        except Exception, e:
            self.fail("RestServer did not initialize. Unexpected error: {0}"
                .format(e.message))

    def test_register_route(self):
        server = initialize()
        server.register_route(urlpatterns=["/.*"], verbs=["GET"])

if __name__ == '__main__':
    RestServerTests().main(sys.argv[1:])

