#!/bin/env python
import sys
sys.path.append('../../../../../oldpeculier/')
import unittest
from oldpeculier.base.rest.client import RestClient
from tests.unit.abc import BaseUnitTest
from httplib import HTTPConnection, HTTPSConnection

def initialize(**kargs):
    return RestClient(**kargs)

class RestClientTests(unittest.TestCase,BaseUnitTest):
    def __init__(self,testmethod=None):
        self.url = "://www.amazon.com"
        if testmethod:
            super(RestClientTests,self).__init__(testmethod)

    def test_if_missing_arguments_are_caught(self):
        try:
            client = initialize()
        except ValueError, e:
            self.assertRegexpMatches(e.message,"Argument url is required.*")
        
    def test_if_bad_schemes_are_rejected(self):
        try:
            scheme = "s3"
            initialize(url=scheme+self.url)
            self.fail("Scheme {0} did not cause an exception. This was not expected."
                .format(scheme));
        except ValueError, e:
            self.assertRegexpMatches(e.message,"Scheme {0} is not a supported type.*"
                .format(scheme))

    def test_if_good_schemes_are_accepted(self):
        try:
            scheme = "http"
            initialize(url=scheme+self.url)
        except ValueError, e:
            self.fail("Scheme {0} caused an exception. This was not expected."
                .format(scheme));

    def test_if_default_ports_get_assigned(self):
        scheme = "http"
        rest = initialize(url=scheme+self.url)
        self.assertEquals(rest.port,80)
        scheme = "https"
        rest = initialize(url=scheme+self.url)
        self.assertEquals(rest.port,443)

    def test_if_custom_ports_are_accepted(self):
        scheme = "https"
        rest = initialize(url=scheme+self.url+":8000")
        self.assertEquals(rest.port,8000)

    def test_if_an_agent_is_created(self):
        scheme = "http"
        rest = initialize(url=scheme+self.url)
        self.assertIsInstance(rest.agent,HTTPConnection)

        scheme = "https"
        rest = initialize(url=scheme+self.url)
        self.assertIsInstance(rest.agent,HTTPSConnection)

    def test_that_url_overrides_all(self):
        scheme = "http"
        port = 80
        rest = initialize(url="https"+self.url+":8888",scheme=scheme,port=port)
        self.assertEquals(rest.port,8888)
        self.assertEquals(rest.scheme,"https")

if __name__ == '__main__':
    RestClientTests().main(sys.argv[1:])
