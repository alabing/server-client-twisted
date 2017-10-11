import socket, time
import os, sys, threading

def Send(sock):
	for i in range(100):
		p1 = b'\x26\x00\x00\x00\x00\x10\x00\x01\x0c\x0c\x0c\x0c\x0c\x0c\x00\x00\x00\x0c\x0c\x0c\x0c\x0c\x0c\x00'
		p2 = b'\x10\x00\xfe\xff\x00\x00\x00\x01\x02\x03\x00\x00\x0c\x0c\x0c\x0c\x0c\x0c'
		#p1 = b'\x29\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x0c\x0c\x0c\x0c\x0c\x0c\x00\x00'
		#p2 = b'\x13\x00'+b'type='+b'\xfe\xff'+b';'+b'extype='+b'\x00\x03\x02\x03'
		sock.send(p1+p2)
		time.sleep(1)

def Recv(sock):
	while True:
		data = sock.recv(1024)
		print(data)
		if len(data) == 0:
			break

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM,)
sock.connect(('',8020))
send_t = threading.Thread(target = Send, args = (sock, ), name = 'snedThread', daemon = True)
recv_t = threading.Thread(target = Recv, args = (sock, ), name = 'recvThread', daemon = True)
send_t.start()
recv_t.start()
send_t.join()
recv_t.join()
