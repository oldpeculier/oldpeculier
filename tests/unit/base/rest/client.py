#!/bin/env python
import sys
sys.path.append('../../../../../oldpeculier/')
import unittest
from oldpeculier.base.rest.client import RestClient
from httplib import HTTPConnection, HTTPSConnection

def initialize(**kargs):
    return RestClient(**kargs)

class RestClientTests(unittest.TestCase):
    def __init__(self,testmethod):
        self.url = "://www.amazon.com"
        super(RestClientTests,self).__init__(testmethod)

    def test_if_bad_schemes_are_rejected(self):
        try:
            scheme = "s3"
            initialize(url=scheme+self.url)
            self.fail("Scheme {0} did not cause an exception. This was not expected.".format(scheme));
        except ValueError, e:
            self.assertRegexpMatches(e.message,"Scheme {0} is not a supported type.*".format(scheme))

    def test_if_good_schemes_are_accepted(self):
        try:
            scheme = "http"
            initialize(url=scheme+self.url)
        except ValueError, e:
            self.fail("Scheme {0} caused an exception. This was not expected.".format(scheme));

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

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(RestClientTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
