#!/bin/env python
import re
from httplib import HTTPConnection, HTTPSConnection
from urlparse import urlparse
class BaseRest():
    def __init__(self, **args):
        self.__required_arguments=['url']
        for key, value in args.items():
            setattr(self,key,value)
        for argument in self.__required_arguments:
            try:
                getattr(self,argument)
            except AttributeError:
                raise ValueError("Argument {0} is required as a constructor for class {1}".format(argument,self.__class__))

        if re.search('^https://',self.url):
            self.agent = HTTPSConnection(self.url,self.port)
        elif re.search('^http://',self.url):
            self.agent = HTTPConnection(self.url,self.port)
        else:
            raise ValueError("{0} is not a valid url.".format(self.url))
    
        
