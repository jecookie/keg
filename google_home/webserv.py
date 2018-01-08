#!/usr/bin/env python
"""
Very simple HTTP server in python.
Usage::
    ./dummy-web-server.py [<port>]
Send a GET request::
    curl http://localhost
Send a HEAD request::
    curl -I http://localhost
Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost
"""
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import urlparse
import eiscp


class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write("<html><body><h1>hi!</h1></body></html>")

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        length = int(self.headers.getheader('content-length'))
        field_data = self.rfile.read(length)
        fields = urlparse.parse_qsl(field_data)

        print fields
        print type(fields)
        print fields[0][0]

        
        if 'power' in fields[0]:
            key=fields[0][1]

            # Create a receiver object, connecting to the host
            receiver = eiscp.eISCP('192.168.2.109')

            # Turn the receiver on, select PC input
            receiver.command('power '+key)
            receiver.disconnect()

            print "receive on. source " + src + ". volume 40"
        

        if 'source' in fields[0]:
            src=fields[0][1]
            print "Setting source to " + src

            # Create a receiver object, connecting to the host
            receiver = eiscp.eISCP('192.168.2.109')

            # Turn the receiver on, select PC input
            receiver.command('power on')
            receiver.command('source '+src)
            receiver.command('volume 40')
            receiver.disconnect()

            print "receive on. source " + src + ". volume 40"
        



def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()

