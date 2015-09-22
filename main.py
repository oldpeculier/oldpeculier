#!/usr/bin/env python
import sys
import signal
from oldpeculier.base.rest.server import RestServer, RestHandler
from oldpeculier.base.rest.client import RestClient
#b = Rest(url="https://www.google.com", port=123, protocol="https")
#print b.url
#print dir(b.agent)
def handler(request):
    request.send_response(200)
    request.end_headers()
    message = "sup"
    request.wfile.write(message)
    request.wfile.write('\n')

def handler2(request):
    request.send_response(200)
    request.end_headers()
    message = "nah"
    request.wfile.write(message)
    request.wfile.write('\n')

#server.register_route(urlpatterns=[],methods=[],handler=handler)
server = RestServer(logger_level='warning')#, logger_location='/tmp/oldpeculier2')
server.logger.warning("did this work?")
server.register_route(["/.*"],["GET"],handler)
server.register_route(["/secure/.*","/nonsecure/.*"],["GET"],handler2)
#def somethingelse(signal,frame):
#    print "hello"
#    server.server_shutdown(signal,frame)
#    sys.exit(0)

#signal.signal(signal.SIGINT,somethingelse)
#server.serve_forever()
