#!/bin/env python
import sys
sys.path.append('../../../../oldpeculier/')
import unittest
from oldpeculier.base.rest import Rest

def initialize(**args):
    Rest(**args)

class InitializationTests(unittest.TestCase):
    def test_if_bad_scheme_is_rejected(self):
        try:
            scheme = "s3"
            url = scheme + "://www.amazon.com"
            initialize(url=url)
            self.fail("Scheme {0} did not cause an exception. This was not expected.".format(scheme));
        except ValueError, e:
            self.assertRegexpMatches(e.message,"Scheme {0} is not a supported type.*".format(scheme))

    def test_if_good_scheme_is_accepted(self):
        try:
            scheme = "http"
            url = scheme + "://www.amazon.com"
            initialize(url=url)
        except ValueError, e:
            self.fail("Scheme {0} caused an exception. This was not expected.".format(scheme));

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(InitializationTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
