#!/bin/env python
import re
import sys
from httplib import HTTPConnection, HTTPSConnection
from urlparse import urlparse
#sys.path.append('../../../oldpeculier')
from oldpeculier.common import Common

__version__ = '0.0.1'

#----------------------------------------------------------------------------------------#
# Constructors
#----------------------------------------------------------------------------------------#
# RestClient(url=<type str>)
# Restclient(scheme=<type str>, port=<type int>, url=<type str>)
# 
# If a port or scheme is include in the url argument, it will override all

class RestClient(Common):
    __required_arguments = ['url']
    __protected_arguments = ['agent']
    def __init__(self, **args):
        Common.__init__(self, **args)
        url = urlparse(self.url)
        if url.scheme == '':
            self.scheme="http"
        else:
            setattr(self,"scheme",url.scheme)

        if re.search('^https$',self.scheme):
            if url.port:
                self.port=url.port
            else:
                self.port=443
            self.agent = HTTPSConnection(url.hostname,self.port)
        elif re.search('^http$',self.scheme):
            if url.port:
                self.port=url.port
            else:
                self.port=80
            self.agent = HTTPConnection(url.hostname,self.port)
        else:
            raise ValueError("Scheme {0} is not a supported type for class {1}"
                .format(self.scheme,type(self).__name__))
         
