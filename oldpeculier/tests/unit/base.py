#!/bin/env python
import sys
import unittest
class BaseUnitTest(object):
    def main(self,tests=[]):
        try:
            if len(tests) == 0:
                suite = unittest.TestLoader().loadTestsFromTestCase(self.__class__)
                unittest.TextTestRunner(verbosity=2).run(suite)
            else:
                suite = unittest.TestSuite()
                for test in tests:
                    suite.addTest(self.__class__(test))
                unittest.TextTestRunner(verbosity=2).run(suite)
        except Exception,e:
            print e.message

