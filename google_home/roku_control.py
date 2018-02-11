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
#curl -d '' http://192.168.2.102:8060/keypress/home
#curl -d '' http://192.168.2.102:8060/keypress/power
#https://sdkdocs.roku.com/display/sdkdoc/External+Control+API#ExternalControlAPI-KeypressKeyValues


from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import urlparse
import requests


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
        #print type(fields)
        #print fields[0][0]
#Turn On/Off the TV
##control on/off (powerOn/PowerOff)
#Set the TV to ___ (InputTuner, InputHDMI1
##  input __
###launch/12 - Netflix
#See http://192.168.2.102:8060/query/apps  full list of apps
        toSend=""
        if 'control' in fields[0]:
            #On/Off
            key=fields[0][1].lower().lstrip().split(' ',1)[0]

            if 'on' in key:
                toSend = "keypress/PowerOn"
            elif 'off' in key:
                toSend = "keypress/PowerOff"
                
            
            print "TV " + key
        

        if 'source' in fields[0]:
            src=fields[0][1].lower().lstrip()
            print "receive on. source " + src + ". volume 35"

        cmd =  "http://192.168.2.102:8060/" + toSend
        print cmd
        r = requests.post( cmd, data = {} )
        print(r.status_code, r.reason)
        print(r.text[:300] + '...')


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


