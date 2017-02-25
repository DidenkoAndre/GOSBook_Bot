from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import subprocess
import json

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        content_len = int(self.headers.getheader('content-length')) 
        post_body = self.rfile.read(content_len)
        answer = json.loads(post_body)
        commit_message = answer['head_commit']['message']
        pull = subprocess.Popen(['make'])
        broadcast = subprocess.Popen(['python', 'broadcast.py', commit_message])

def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('0.0.0.0', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
