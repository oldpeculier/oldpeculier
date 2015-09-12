#!/usr/bin/env python
import logging
import re
class Common(object):
    def __init__(self, **args):
        logger = logging.getLogger('abc')

        if hasattr(self,'logger_location'):
            handler = logging.FileHandler(args['logger_location'])
            del self.logger_location
        else:
            handler = logging.FileHandler('/tmp/oldpeculier.log')

        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        handler.setFormatter(formatter) 
        logger.addHandler(handler)
        if hasattr(self,'logger_level'):
            if re.search('^info$',args['logger_level'],re.IGNORECASE): 
                logger.setLevel(logging.INFO)
            elif re.search('^(warn|warning)$',args['logger_level'],re.IGNORECASE):
                logger.setLevel(logging.WARNING)
            else:
                logger.setLevel(logging.WARNING)
            self.logger = logging.getLogger('abc')
            del self.logger_level

