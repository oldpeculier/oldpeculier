#!/bin/env python
import sys
sys.path.append('../../../../oldpeculier/')
import unittest
from oldpeculier.base.common import Common

def initialize(**kargs):
    return Common(**kargs)
    
class CommonTests(unittest.TestCase):
    def __init__(self,testmethod):
        super(Common,self).__init__(testmethod)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(RestClientTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
