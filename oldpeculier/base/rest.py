#!/bin/env python
import re
from httplib import HTTPConnection, HTTPSConnection
from urlparse import urlparse
class Rest():
    def __init__(self, **args):
        self.__required_arguments=['url']
        for key, value in args.items():
            setattr(self,key,value)
        for argument in self.__required_arguments:
            try:
                getattr(self,argument)
            except AttributeError:
                raise ValueError("Argument {0} is required as a constructor for class {1}".format(argument,self.__class__))
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
                raise ValueError("Scheme {0} is not a supported type for class {1}".format(self.scheme,self.__class__))
