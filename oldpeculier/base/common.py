#!/usr/bin/env python
import logging
import re
import sys

class Common(object):
    def __init__(self, **kwargs):
        required_arguments = []
        protected_arguments = []
        required_arguments_key = "_{0}__required_arguments".format(type(self).__name__)
        protected_arguments_key = "_{0}__protected_arguments".format(type(self).__name__)

        if hasattr(self,required_arguments_key):
            required_arguments = getattr(self,required_arguments_key)

        if hasattr(self,protected_arguments_key):
            protected_arguments=getattr(self,protected_arguments_key)

        protected_arguments="^{0}$".format("|".join(protected_arguments))

        for key, value in kwargs.items():
            if not re.search(protected_arguments,key):
                setattr(self,key,value)

        for argument in required_arguments:
            try:
                getattr(self,argument)
            except AttributeError:
                raise ValueError("Argument {0} is required as a constructor for class {1}"
                    .format(argument,type(self).__name__))

        if hasattr(self, 'logger_name'):
            self.logger = logging.getLogger(kwargs['logger_name'])
            del self.logger_name
        else:
            self.logger = logging.getLogger(self.__class__.__name__)

        if hasattr(self,'logger_location'):
            handler = logging.FileHandler(kwargs['logger_location'])
            del self.logger_location
        else:
            handler = logging.StreamHandler(sys.stdout)

        formatter = logging.Formatter('%(levelname)s [PID:%(process)d] %(asctime)s '
            + '[FILE:%(pathname)s:%(lineno)d] - %(message)s')
        handler.setFormatter(formatter) 
        self.logger.addHandler(handler)
        if hasattr(self,'logger_level'):
            if re.search('^debug$',kwargs['logger_level'],re.IGNORECASE): 
                self.logger.setLevel(logging.DEBUG)
            elif re.search('^info$',kwargs['logger_level'],re.IGNORECASE):
                self.logger.setLevel(logging.INFO)
            elif re.search('^(warn|warning)$',kwargs['logger_level'],re.IGNORECASE):
                self.logger.setLevel(logging.WARNING)
            elif re.search('^(err|error)$',kwargs['logger_level'],re.IGNORECASE):
                self.logger.setLevel(logging.ERROR)
            elif re.search('^critical$',kwargs['logger_level'],re.IGNORECASE):
                self.logger.setLevel(logging.CRITICAL)
            else:
                self.logger.setLevel(logging.WARNING)
            del self.logger_level
