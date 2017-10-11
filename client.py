from twisted.internet.protocol import ClientFactory, ServerFactory, Protocol
from twisted.internet import reactor
import sys, select

connected = 1

def prompt() :
    sys.stdout.write('<You> ')
    sys.stdout.flush()

def readStdin():
	while 1:
		socket_list = [sys.stdin,]
		# Get the list sockets which are readable
		read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
		for sock in read_sockets:
			msg = sys.stdin.readline()
			prompt()
		if connected == 0:
			break

	

class myProtocol(Protocol):
	def connectionMade(self):
		self.transport.write(b"show -g\n")
		print("Connected to %s."%self.transport.getPeer().host)
		connected = 1
		

	def dataReceived(self, data):
		print(data)
		#line = sys.stdin.readline() 

	def connectionLost(self, reason):
		connected = 0
	
	

class myFactory(ClientFactory):
	protocol = myProtocol
	def __init__(self, name):
		self.name = name
	
	def clientConnectionLost(self, connector, reason): 
		print('Failed to connect to:', connector.getDestination())

def main():
	factory = myFactory("client")
	reactor.connectTCP("127.0.0.1", 8010, factory)
	#reactor.callInThread(readStdin)
	reactor.run()

if __name__ == '__main__':
	main()
