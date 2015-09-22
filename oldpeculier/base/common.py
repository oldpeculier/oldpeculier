#!/usr/bin/env python
import logging
import re
import sys

class Common(object):
    def __init__(self, **args):
        if hasattr(self, 'logger_name'):
            self.logger = logging.getLogger(args['logger_name'])
            del self.logger_name
        else:
            self.logger = logging.getLogger(self.__class__.__name__)

        if hasattr(self,'logger_location'):
            handler = logging.FileHandler(args['logger_location'])
            del self.logger_location
        else:
            handler = logging.StreamHandler(sys.stdout)

        formatter = logging.Formatter('%(levelname)s [PID:%(process)d] %(asctime)s [FILE:%(filename)s:%(lineno)d] - %(message)s')
        handler.setFormatter(formatter) 
        self.logger.addHandler(handler)
        if hasattr(self,'self.logger_level'):
            if re.search('^debug$',args['self.logger_level'],re.IGNORECASE): 
                self.logger.setLevel(logging.DEBUG)
            elif re.search('^info$',args['self.logger_level'],re.IGNORECASE):
                self.logger.setLevel(logging.INFO)
            elif re.search('^(warn|warning)$',args['self.logger_level'],re.IGNORECASE):
                self.logger.setLevel(logging.WARNING)
            elif re.search('^(err|error)$',args['self.logger_level'],re.IGNORECASE):
                self.logger.setLevel(logging.ERROR)
            elif re.search('^critical$',args['self.logger_level'],re.IGNORECASE):
                self.logger.setLevel(logging.CRITICAL)
            else:
                self.logger.setLevel(logging.WARNING)
            del self.logger_level

