#!/bin/env python
import re
import sys
from httplib import HTTPConnection, HTTPSConnection
from urlparse import urlparse
sys.path.append('../../../../oldpeculier')
from oldpeculier.base.common import Common

__version__ = '0.0.1'

#----------------------------------------------------------------------------------------#
# Constructors
#----------------------------------------------------------------------------------------#
# RestClient(url=<type str>)
# Restclient(scheme=<type str>, port=<type int>, url=<type str>)
# 
# If a port or scheme is include in the url argument, it will override all

class RestClient(Common):
    def __init__(self, **args):
        self.__required_arguments = ['url']
        self.__protected_arguments = ['agent']
        Common.__init__(self, **args)

        url = urlparse(self.url)
        if url.scheme == '':
            self.scheme="http"
        else:
            setattr(self,"scheme",url.scheme)
       
        if url.port:
            self.port=url.port
        else:
            if re.search('^https$',self.scheme):
                self.port=443
                self.agent = HTTPSConnection(self.url,self.port)
            elif re.search('^http$',self.scheme):
                self.port=80
                self.agent = HTTPConnection(self.url,self.port)
            else:
                raise ValueError("Scheme {0} is not a supported type for class {1}"
                    .format(self.scheme,type(self).__name__))
