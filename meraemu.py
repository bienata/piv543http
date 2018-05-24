import socket
from datetime import datetime

# zapozyczka forumowa
# https://stackoverflow.com/questions/22586286/python-is-there-an-equivalent-of-mid-right-and-left-from-basic	
def left(s, amount = 1, substring = ""):
    if (substring == ""):
        return s[:amount]
    else:
        if (len(substring) > amount):
            substring = substring[:amount]
        return substring + s[:-amount]

def right(s, amount = 1, substring = ""):
    if (substring == ""):
        return s[-amount:]
    else:
        if (len(substring) > amount):
            substring = substring[:amount]
        return s[:-amount] + substring	

# --- emulatorek scpi ---		
		
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind( ( "", 5555) )
s.listen( 1 )

while 1:
	print "waiting for command"
	conn, addr = s.accept()
	data = conn.recv(1024)
	cmd = data.decode().strip()
	print "rx: ", cmd
	
	if cmd == "*idn?":
		resp = "Emulated Meratronik V543 SCPI Interface, tasza"

	elif cmd == ":meter:mode?":
		resp = "0|DC"

	elif cmd == ":meter:v:range?":
		resp = "0|10V|1000"
		
	elif cmd == ":meter:display?":
		sec = datetime.now().second
		pol = "-"
		if bool( sec & 1 ): pol = "+"
		sec *= 2
		if sec == 120: sec = 119		
		resp = pol + right( "000" + str( sec ), 3) + right( "00" + str(sec), 2)
		
	else:
		resp = "error"	
		
	conn.sendall( resp.encode() )
	print "tx: ", resp	
	conn.close()
    
