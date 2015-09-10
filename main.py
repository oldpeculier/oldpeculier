#!/bin/env python
from oldpeculier.base.rest import BaseRest
b = BaseRest(url="https://www.google.com", port=123, protocol="https")
print b.url
print dir(b.agent)
