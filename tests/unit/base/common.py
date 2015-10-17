#!/bin/env python
import sys
sys.path.append('../../../../oldpeculier/')
import unittest
import logging
import tempfile
from cStringIO import StringIO
from oldpeculier.base.common import Common

def initialize(**kargs):
    return Common(**kargs)
    
class CommonTests(unittest.TestCase):
    def __init__(self,testmethod):
        super(CommonTests,self).__init__(testmethod)

    def test_that_attributes_are_inherited(self):
        common = initialize(first="one",second="two")
        self.assertEquals(common.first,"one")
        self.assertEquals(common.second,"two")

    def test_setting_logger_properties(self):
        common = initialize()
        self.assertIsInstance(common.logger.handlers[0],logging.StreamHandler)
        self.assertEquals(common.logger.getEffectiveLevel(),logging.WARNING)
        common.logger.handlers=[]

        common = initialize(logger_location='/dev/null',logger_name='test',
            logger_level='info')
        self.assertEquals(common.logger.name,'test')
        self.assertEquals(common.logger.handlers[0].baseFilename,'/dev/null')
        self.assertEquals(common.logger.getEffectiveLevel(),logging.INFO)
        common.logger.handlers=[]

        common = initialize(logger_location='/dev/null',logger_name='test',
            logger_level='debug')
        self.assertEquals(common.logger.getEffectiveLevel(),logging.DEBUG)
        common.logger.handlers=[]

        common = initialize(logger_location='/dev/null',logger_name='test',
            logger_level='warning')
        self.assertEquals(common.logger.getEffectiveLevel(),logging.WARNING)
        common.logger.handlers=[]

        common = initialize(logger_location='/dev/null',logger_name='test',
            logger_level='error')
        self.assertEquals(common.logger.getEffectiveLevel(),logging.ERROR)
        common.logger.handlers=[]

        common = initialize(logger_location='/dev/null',logger_name='test',
            logger_level='critical')
        self.assertEquals(common.logger.getEffectiveLevel(),logging.CRITICAL)
        common.logger.handlers=[]

    def test_formatting_of_the_logger(self):
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        common = initialize()
        common.logger.warning("test 123 321 tset")
        sys.stdout = old_stdout
        self.assertRegexpMatches(mystdout.getvalue(),
            "^WARNING \[PID:.*\] .* \[FILE:common.py:.*\] - test 123 321 tset$")
        common.logger.handlers=[]

    def test_logger_writes_to_the_specified_file(self):
        f = tempfile.NamedTemporaryFile(delete=True)
        common = initialize(logger_location=f.name)
        self.assertEquals(common.logger.handlers[0].baseFilename,f.name)
        common.logger.warning("test 123 321 tset")
        lines = tuple(open(f.name,'r'))
        self.assertRegexpMatches(lines[0],
            "^WARNING \[PID:.*\] .* \[FILE:common.py:.*\] - test 123 321 tset$")

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(CommonTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
