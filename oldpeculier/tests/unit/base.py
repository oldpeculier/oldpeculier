#!/bin/env python
import sys
import unittest
import re

class BaseUnitTest(object):
    def get_log_level(self,args):
        loglevel='warn'
        for arg in args:
            if arg == "--debug":
                loglevel='debug'
            elif arg == "--info":
                loglevel='info'
        return loglevel

    def main(self,tests=[]):
        loglevel = self.get_log_level(tests)
        tests = [test for test in tests if test.startswith("test") ]
        try:
            methods=dir(self.__class__)
            if len(tests) == 0:
                tests = [test for test in methods if test.startswith("test") ]
            suite = unittest.TestSuite()
            for test in tests:
                suite.addTest(self.__class__(test,loglevel))
            unittest.TextTestRunner(verbosity=2).run(suite)
        except Exception,e:
            print e.message
