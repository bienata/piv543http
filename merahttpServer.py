#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
from datetime import datetime
import socket

def scpiCall( cmd ):
	s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
	s.connect( ("neonowy", 5555) )
	s.sendall( cmd.encode() )
	resp = s.recv( 1024 )
	s.close()
	return resp.decode().strip()	

def processInfoPage( p ):
	p = p.replace( "$IDN$", 	scpiCall( "*idn?"			) )
	p = p.replace( "$MODE$", 	scpiCall( ":meter:mode?"	) )		
	p = p.replace( "$RANGE$", 	scpiCall( ":meter:v:range?"	) )	
	p = p.replace( "$DISPLAY$", scpiCall( ":meter:display?"	) )	
	return p


class myHandler( BaseHTTPRequestHandler ):
    
	def do_GET(self):	
		if self.path == "/info" or self.path == "/":	# info page, root page
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			f = open( curdir + sep + 'info.html' )
			t1 = datetime.now()			
			pg = processInfoPage ( f.read() )
			t2 = datetime.now()						
			pg += "<br><center><font size=2>generated in: " + str( int((t2-t1).total_seconds()*1000) ) + " ms</font>"
			self.wfile.write( pg )
			f.close()            
			
		elif self.path == "/meter":			# analog meter demo                
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			f = open( curdir + sep + 'meter.html' )                 
			self.wfile.write( f.read() )
			f.close()    
			
		elif self.path == "/meterData":		# ajax calls
			self.send_response(200)
			self.send_header('Content-type','text/plain')
			self.end_headers()
			self.wfile.write( scpiCall( ":meter:display?" ) )
			
		else:
			self.wfile.write(":(")
		return
try:
    server = HTTPServer( ('', 8080), myHandler )
    server.serve_forever()

except KeyboardInterrupt:
    print 'Ctrl+C - exit now!'
    server.socket.close()
    