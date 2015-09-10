#!/usr/bin/env python
from oldpeculier.base.rest import Rest
b = Rest(url="https://www.google.com", port=123, protocol="https")
print b.url
print dir(b.agent)
