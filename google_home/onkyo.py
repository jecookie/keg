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

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False


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
        print fields[0]
        print fields[0][0]
        task = fields[0][0].lower().lstrip()
        key=fields[0][1].lower().lstrip().split(' ',1)[0]
        #print type(fields)
        #print fields[0][0]

#todo
#get the IP address 
#control the volume
#set default volume based on source
#control the TV
        
        if 'control' in task:
            #On/Off

            # Create a receiver object, connecting to the host
            receiver = eiscp.eISCP('192.168.2.100')
            if 'on' in key or 'off' in key:
                # Turn the receiver on, select PC input
                receiver.command('power '+key)
            elif 'up' in key or 'down' in key:
                #forward volume up/down commands
                task='volume'
                print "volume cmd"

            receiver.disconnect()

            print "receiver " + key
        

        if 'source' in task:
            if 'music' in key:
                key='pc'
            elif 'tv' in key:
                key='tv/cd'
            elif 'playstation' in key:
                key='game'
            elif 'ps3' in key:
                key='game'



            print "Setting source to " + key

            # Create a receiver object, connecting to the host
            receiver = eiscp.eISCP('192.168.2.100')

            # Turn the receiver on, select PC input
            receiver.command('power on')
            receiver.command('source '+src)
            receiver.command('volume 35')
            receiver.disconnect()

            print "receive on. source " + src + ". volume 35"

        if 'volume' in task:
            print "key='"+key+"'"
            receiver = eiscp.eISCP('192.168.2.100')
            if 'up' in key or 'down' in key:
                print "volume " + key + " x5"
                print 'volume level-'+key
                receiver.command('volume level-'+key)
                receiver.command('volume level-'+key)
                receiver.command('volume level-'+key)
                receiver.command('volume level-'+key)
                receiver.command('volume level-'+key)
            elif 'mute' in key:
                receive.command('mute')
                print "muted"
            
            elif RepresentsInt(key):
                if key > 50:
                    key = 50
                receiver.command('volume '+key)
                print "volume set to " + key
            else:
                print "volume key not recognized '"+key+"'"
                    


                
            receiver.disconnect()
            
        



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

