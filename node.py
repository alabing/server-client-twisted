import function, protocol
import time,struct

class Node:
	def __init__(self):
		self.clientDict = {}
		self.gatewayDict = {}

	#-------------------------client--------------------------
	def getClientName(self, node):
		for name in self.clientDict:
			if self.clientDict[name] == node:
				return name

	def addClientNode(self, node):
		name = function.createName("client")
		self.clientDict[name] = node

	def delClientNode(self, node):
		for name in list(self.clientDict):
			if self.clientDict[name] == node:
				del self.clientDict[name]
				node.transport.loseConnection()

	def clientInitialize(self, node):
		node.clientIP = node.transport.getPeer().host
		self.addClientNode(node)
		node.clientName = self.getClientName(node)
		self.echoClient(node)
		for name in self.gatewayDict:
			if self.gatewayDict[name].attPackage:
				node.transport.write(self.gatewayDict[name].attPackage)
	
	def echoClient(self, node):
		print('-----------------------------------------')
		print('%s       %s' %(node.clientName,node.clientIP))

	def start_spec(self,dstID,msg,node):
		if self.gatewayDict:
			for name in self.gatewayDict:
				if self.gatewayDict[name].nodeID == dstID:
					node.isRecvSpec = True
					self.gatewayDict[name].transport.write(msg)

	def stop_spec(self,dstID,msg,node):
		if self.gatewayDict:
			for name in self.gatewayDict:
				if self.gatewayDict[name].nodeID == dstID:
						node.isRecvSpec = False
						self.gatewayDict[name].transport.write(msg)

	def trans_cmd(self,dstID,msg,node):
		if self.gatewayDict:
			for name in self.gatewayDict:
				if self.gatewayDict[name].nodeID == dstID:
					self.gatewayDict[name].transport.write(msg)

	#-----------------------gateway---------------------
	def getGatewayName(self, node):
		for name in self.gatewayDict:
			if self.gatewayDict[name] == node:
				return name

	def addGatewayNode(self, node):
		name = function.createName("gateway")
		self.gatewayDict[name] = node

	def delGatewayNode(self, node):
		for name in list(self.gatewayDict):
			if self.gatewayDict[name] == node:
				print('%s is lost'%name)
				node.check_task.stop()
				node.beat_task.stop()
				del self.gatewayDict[name]
				node.transport.loseConnection()
				#self.broadcast(self.drop_msg(node))

	def gatewayInitialize(self,node):
		node.gatewayIP = node.transport.getPeer().host
		self.addGatewayNode(node)
		node.gatewayName = self.getGatewayName(node)
		self.echoGateway(node)

	def send_spec(self, msg):
		if self.clientDict:
			for name in self.clientDict:
				if self.clientDict[name].isRecvSpec:
					self.clientDict[name].transport.write(msg)

	def broadcast(self, msg):
		if self.clientDict:
			for name in self.clientDict:
				self.clientDict[name].transport.write(msg)
	
	def echoGateway(self, node):
		print('----------------------------------------------------------------------')
		print('%s       %s         ' %(node.gatewayName,node.gatewayIP),end='')

	def createHeartbeat(self, node):
		total_len = 41
		ptl_ID = 0
		gateway_do = 0
		prio = 0
		ndst = 1
		srcID = b'\x00\x00\x00\x00\x00\x00\x00\x00'
		dstID = node.nodeID
		data_len = 19
		data_buf = b'type='+b'\xfe\xff'+b';'+b'extype='+b'\x00\x03\x02\x03'
		heartbeat = struct.pack('i4B8s8sh19s',total_len, ptl_ID, gateway_do, prio, ndst, srcID, dstID, data_len,data_buf)
		return heartbeat

	def sendHeartbeat(self, node):
		if not node.nodeID:
			pass
		else:
			heartbeat = self.createHeartbeat(node)
			node.transport.write(heartbeat)

	def checkConnect(self, node):
		if node.heartbeat_time != 0 and int(time.time())-node.heartbeat_time >20:
			self.delGatewayNode(node)

	def drop_msg(self,node): #!!!!!!!!!!!
		ptl_ID = 0
		gateway_do = 1
		prio = 0
		ndst = 1
		srcID = node.nodeID
		dstID = b'\x00\x00\x00\x00\x00\x00\x00\x00'
		data_len = 8    #!
		type_ = 0xfffe  #!
		extype = protocol.DROP
		packet = struct.pack('4B8s8shHi',ptl_ID, gateway_do, prio, ndst, srcID, dstID, data_len,type_,extype)
		total_len = struct.pack('i',len(packet))
		return total_len+packet

		
