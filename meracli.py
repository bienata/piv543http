#!/usr/bin/python
import socket

s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
s.connect( ("neonowy", 5555) )
s.sendall( ":meter:display?" )
resp = s.recv( 1024 )
s.close()
print "Response [", resp.strip() , "]"

s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
s.connect( ("neonowy", 5555) )
s.sendall( "*idn?" )
resp = s.recv( 1024 )
s.close()
print "Response [", resp.strip() , "]"

s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
s.connect( ("neonowy", 5555) )
s.sendall( ":meter:mode?" )
resp = s.recv( 1024 )
s.close()
print "Response [", resp.strip() , "]"

s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
s.connect( ("neonowy", 5555) )
s.sendall( ":meter:v:range?" )
resp = s.recv( 1024 )
s.close()
print "Response [", resp.strip() , "]"


