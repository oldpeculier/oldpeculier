#!/bin/env python
import sys
sys.path.append('../../../../../oldpeculier/')
import unittest
from oldpeculier.base.rest.server import RestServer
from httplib import HTTPConnection, HTTPSConnection

def initialize(**kargs):
    return RestServer(**kargs)

class RestServerTests(unittest.TestCase):
    def __init__(self,testmethod):
        super(RestServerTests,self).__init__(testmethod)
    
    def test_initialize(self):
        try:
            initialize()
        except Exception, e:
            self.fail("RestServer did not initialize. Unexpected error: {0}".format(e.message))

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(RestServerTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
