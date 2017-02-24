from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import subprocess
import os

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
        os.chdir("/home/ec2-user/GOS_book/")
        pull = subprocess.Popen(['git','pull','origin'])
        proc = subprocess.Popen(['pdflatex', 'GOSBook.tex'])
        proc.communicate()
        if proc.returncode == 0:
            proc2 = subprocess.Popen(['pdflatex', 'GOSBook.tex'])
            proc2.communicate()
            os.chdir("/home/ec2-user/gosbookbot")
            broadcast = subprocess.Popen(['python','broadcast.py'])
            broadcast.communicate()
        
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
