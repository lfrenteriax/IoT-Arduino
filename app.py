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
#!/usr/bin/python
from http.server import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import cgi
import thread
import threading
import time
import os
import urlparse
from time import gmtime, strftime

blink = True
mydata={'sensorValue':'none','time':'none'}

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
	
	#Handler for the GET requests
	def do_GET(self):
		self.send_response(200)
		if "?" in self.path:
			data=dict(urlparse.parse_qsl(self.path.split("?")[1], True))
			for key,value in dict(urlparse.parse_qsl(self.path.split("?")[1], True)).items():
				print (key + " = " + value)
			print ('data',data)
			print ('mydata', mydata)
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

	#Handler for the POST requests
	def do_POST(self):
		global blink

		#if self.path=="/blink":
		if True:
			form = cgi.FieldStorage(
				fp=self.rfile, 
				headers=self.headers,
				environ={'REQUEST_METHOD':'POST',
		                 'CONTENT_TYPE':self.headers['Content-Type'],
			})

			if (form["cmd"].value=="stop blinking"):
				print ("Stop blinking")
				blink=False
			else:
				blink=True
				print ("Start blinking")

			#Redirect the browser on the main page 
			self.send_response(302)
			self.send_header('Location','/')
			self.end_headers()

			return			
			
#This is a thread that runs the web server 
def WebServerThread():			
	try:
		#Create a web server and define the handler to manage the
		#incoming request
		server = HTTPServer(('0.0.0.0', PORT_NUMBER), myHandler)
		print ('Started httpserver on port ' , PORT_NUMBER)
		
		#Wait forever for incoming htto requests
		server.serve_forever()

	except KeyboardInterrupt:
		print ('^C received, shutting down the web server')
		server.socket.close()

if __name__ == "__main__":
	port = int(os.environ.get('PORT',5000))
	PORT_NUMBER = port

	# Runs the web server thread
	thread.start_new_thread(WebServerThread,())

	# Use the L1 led on Daisy11 module
	#ledL1=ablib.Daisy11("D2","L1")

	#Forever loop
	while True:
		pass # Check the blink flag
