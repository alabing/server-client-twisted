import socket, time
import os, sys, threading

def Send(sock):
	time.sleep(15)
	p1 = b'\x76\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x0c\x0c\x0c\x0c\x0c\x0c\x00\x00'
	p2 = b'\x60\x00'+b'type='+b'\xfe\xff'+b';'+b'extype='+b'\x00\x01\x01\x01'+b';'+b'times='+b'\x00'+b';'+b'freq='+b'\x00\xe1\xf5\x05\x00'+b';'+b'rbw='+b'\x0f'+b';'+b'ifbw='+b'\x16'+b';'+b'squ='+b'\x00\x2d\xf0'+b';'+b'dem='+b'\x01'+b';'+b'att='+b'\x00'+b';'+b'auto='+b'\x00'+b';'+b'gain='+b'\x0c'+b';'+b'avertime='+b'\x00'
 
	sock.send(p1+p2)
	#for i in range(100):
	#	p1 = b'\x29\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x0c\x0c\x0c\x0c\x0c\x0c\x00\x00'
	#	p2 = b'\x13\x00'+b'type='+b'\xfe\xff'+b';'+b'extype='+b'\x00\x01\x01\x01'
	#	sock.send(p1+p2)
	#	time.sleep(1)

def Recv(sock):
	while True:
		data = sock.recv(1024)
		print(data)
		

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM,)

sock.connect(('',8010))
send_t = threading.Thread(target = Send, args = (sock, ), name = 'sendThread', daemon = True)
recv_t = threading.Thread(target = Recv, args = (sock, ), name = 'recvThread', daemon = True)
send_t.start()
recv_t.start()
send_t.join()
recv_t.join()


#for i in range(100):
#	sock.send(b'1\x00\x02\x00\x00\x00')
#	time.sleep(1)
