# -*- coding: utf-8 -*-
'''
from flask import Flask
app = Flask(__name__)
import os
@app.route("/")
def hello():
    return "Hello leo!"

if __name__ == "__main__":
    port = int(os.environ.get('PORT',5000))
    app.run(host='0.0.0.0', port=port)
'''
'''
from tornado import websocket
import tornado.ioloop

class EchoWebSocket(websocket.WebSocketHandler):
    def open(self):
        print "Websocket Opened"

    def on_message(self, message):
        self.write_message(u"You said: %s" % message)

    def on_close(self):
        print "Websocket closed"

application = tornado.web.Application([(r"/", EchoWebSocket),])

if __name__ == "__main__":
    application.listen(9000)
    tornado.ioloop.IOLoop.instance().start()
'''


import BaseHTTPServer
import urlparse


from time import gmtime, strftime
mydata={'sensorValue':'none','time':'none'}
class SimpleHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    '''
    def do_HEAD(s):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
    '''

    def do_GET(self):
        self.send_response(200)
        if "?" in self.path:
            data=dict(urlparse.parse_qsl(self.path.split("?")[1], True))
            for key,value in dict(urlparse.parse_qsl(self.path.split("?")[1], True)).items():
                print key + " = " + value
            print 'data',data
            print 'mydata', mydata
            myTime=strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
            mydata['time']=myTime
            mydata['sensorValue']=data['sensorValue']
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write('<html><head><title>IoT server.</title><meta http-equiv="refresh" content="5" /></head>')
        try:
            self.wfile.write("<body><p>Sensor value at  "+mydata['time']+" >>>>> "+ mydata["sensorValue"]+"</p>")
        except:
           self.wfile.write("<body><p>Sensor value= none</p>")
        # If someone went to "http://something.somewhere.net/foo/bar/",
        # then s.path equals "/foo/bar/".
        #self.wfile.write("<p>You accessed path: %s</p>" % self.path)
        self.wfile.write("</body></html>")
    def do_POST(self):
        self.send_response(200)
        if self.rfile:
             # print urlparse.parse_qs(self.rfile.read(int(self.headers['Content-Length'])))
             for key,value in dict(urlparse.parse_qs(self.rfile.read(int(self.headers['Content-Length'])))).items():
                 print key + " = " + value[0]

    def log_request(self, code=None, size=None):
        return

if __name__ == "__main__":
    try:
        BaseHTTPServer.HTTPServer(("0.0.0.0", 80), SimpleHandler).serve_forever()
    except KeyboardInterrupt:
        print('shutting down server')
