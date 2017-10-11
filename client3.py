import socket, select, string, sys

host = "127.0.0.1"
port = 8010

def prompt():
	print('>>', end=' ', flush = True)

def main():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		s.connect((host, port))
	except:
		print('Unable to connect')
		sys.exit()
	print('Connected to remote host. Start sending messages')
	prompt()
	while 1:
		socket_list = [sys.stdin, s]
		read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
		for sock in read_sockets:
			if sock == s:
				data = sock.recv(4096)
				if not data :
					print('\nDisconnected from server')
					sys.exit()
				else:
					print(data.decode())
					prompt()
			else:
				msg = sys.stdin.readline()
				s.send(msg.encode())
				

if __name__ == '__main__':
	main()
