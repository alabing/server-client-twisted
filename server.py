from twisted.internet.protocol import ClientFactory, ServerFactory, Protocol
from twisted.internet import reactor, task
import queue, struct
from domsg import doMsg
from node import Node

doMsg = doMsg()
node = Node()

class clientProtocol(Protocol):
	def __init__(self):
		self.clientIP = ''
		self.clientName = ''
		self.isRecvSpec = False

	def connectionMade(self):
		node.clientInitialize(self)

	def connectionLost(self, reason):
		node.delClientNode(self)
		print("%s connection lost..."%self.clientName)

	def dataReceived(self, data):
		doMsg.cmd_manage(node, data, self)

class clientFactory(ServerFactory):
	protocol = clientProtocol
	def __init__(self, name):
		self.name = name


class gatewayProtocol(Protocol):
	def __init__(self):
		self.gatewayName = ''
		self.nodeID = b''
		self.gatewayIP = ''
		self.attPackage = b''
		self.heartbeat_time = 0
		self.beat_task = 0
		self.check_task = 0

	def connectionMade(self):
		node.gatewayInitialize(self)
		self.heartbeat()
		self.checkConnect()

	def connectionLost(self, reason):
		print("%s connection lost..." %self.gatewayName)
		node.delGatewayNode(self)
		
	def dataReceived(self, data):
		doMsg.msg_manage(data,node,self)

	def heartbeat(self):
		self.beat_task = task.LoopingCall(node.sendHeartbeat, self)
		self.beat_task.start(2, now = False)

	def checkConnect(self):
		self.check_task = task.LoopingCall(node.checkConnect, self)
		self.check_task.start(2, now = False)

class gatewayFactory(ServerFactory):
	protocol = gatewayProtocol
	def __init__(self, name):
		self.name =name

def main():
	factory = clientFactory("client")
	factory2 = gatewayFactory("gateway")
	reactor.listenTCP(8010,factory)
	reactor.listenTCP(8020,factory2)
	reactor.run()

if __name__ == '__main__':
	main()
