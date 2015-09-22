#!/bin/env python
import sys
sys.path.append('../../../../oldpeculier/')
import unittest
from oldpeculier.base.common import Common

def initialize(**kargs):
    return Common(**kargs)
    

