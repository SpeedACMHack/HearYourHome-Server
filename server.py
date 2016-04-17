import cgi
from urlparse import parse_qs
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import hashlib

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
        ctype, pdict = cgi.parse_header(self.headers['content-type'])
        if ctype =='multipart/form-data':
            postvars = cgi.parse_multipart(self.rfile, pdict)
        elif ctype =='application/x-www-form-urlencoded':
            length = int(self.headers.getheader('content-length'))
            postvars = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
        # Doesn't do anything with posted data
        self._set_headers()
        action = postvars["action"]
        device = postvars["device-name"]
        time = postvars["timestamp"]
        if action[0] == "newdevice":
            vals = 'action=' + action[0] + 'device=' + device[0] + 'time=' + time[0]
        elif action[0] == "notify":
            self.wfile.write('<html><body><h1>canconfirm</h1></body></html>')
            vals = 'device=' + device[0] + ';time=' + time[0]
            with open("new.out", "w") as output:
                output.write(vals)      
        with open("out.log", "a") as myfile:
            myfile.write(vals)
            
def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        if argv[1] == POST:
            run(port=int(argv))
        else:
            run(port=int(argv[1]))
    else:
        run()