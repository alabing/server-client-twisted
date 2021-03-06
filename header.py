import struct, protocol

class MsgHeader:
	def __init__(self, total_len,ptl_ID,gateway_do,prio,ndst,srcID,dstID):
		self.total_len = total_len
		self.ptl_ID = ptl_ID
		self.gateway_do = gateway_do
		self.prio = prio
		self.ndst = ndst
		self.srcID = srcID
		self.dstID = dstID

class NodeCharactor:
	def __init__(self,type_,extype,devType,netType,DMAC,SMAC,IP,neighborAPsMAC,neighborAPspwr,reserve,satelliteNUM,gpsTime,gpsValue0,gpsValue1,gpsValue2):
		self.type=type_
		self.extype=extype
		self.devType=devType
		self.netType=netType
		self.DMAC=DMAC
		self.SMAC=SMAC
		self.IP=IP
		self.neighborAPsMAC=neighborAPsMAC
		self.neighborAPspwr=neighborAPspwr
		self.reserve=reserve
		self.satelliteNUM=satelliteNUM
		self.gpsTime=gpsTime
		self.gpsValue=[gpsValue0,gpsValue1,gpsValue2]

def getCharactor(msg,ndst):
	head_len = 16 + ndst*8
	type_,extype,devType,netType,DMAC,SMAC,IP,neighborAPsMAC,neighborAPspwr,reserve,satelliteNUM,gpsTime,gpsValue0,gpsValue1,gpsValue2 = struct.unpack('hiBB8s40si40s5s20sB6s3d',msg[head_len+2:])
	nodeCharactor = NodeCharactor(type_,extype,devType,netType,DMAC,SMAC,IP,neighborAPsMAC,neighborAPspwr,reserve,satelliteNUM,gpsTime,gpsValue0,gpsValue1,gpsValue2)
	return nodeCharactor

class HeadAndType:
	def __init__(self,total_len,ptl_ID,gateway_do,prio,ndst,srcID,dstID,data_len,type_,extype,cmd_data_ack):
		self.total_len = total_len
		self.ptl_ID = ptl_ID
		self.gateway_do = gateway_do
		self.prio = prio
		self.ndst = ndst
		self.srcID = srcID
		self.dstID = dstID
		self.data_len = data_len
		self.type = type_
		self.extype = extype
		self.cmd_data_ack=cmd_data_ack

def getHeadAndType(msg):
	total_len, ptr_ID, gateway_do, prio, ndst, srcID = struct.unpack('i4B8s', msg[:16])
	cmd_data_ack = gateway_do>>4 & 0x03
	head_len = 16 + ndst * 8
	dstID, data_len = struct.unpack('%dsh'%8*ndst, msg[16:head_len+2])
	if cmd_data_ack == protocol.CMD:
		typeIndex = msg.index(b'type=')
		type_, = struct.unpack('i', msg[typeIndex+len(b'type='):typeIndex+len(b'type=')+4])
		extypeIndex = msg.index(b'extype=')
		extype, = struct.unpack('i', msg[extypeIndex+len(b'extype='):extypeIndex+len(b'extype=')+4])
	else:
		 type_, extype = struct.unpack('2i', msg[head_len+2:head_len+2+8])
	headAndType = HeadAndType(total_len,ptr_ID,gateway_do,prio,ndst,srcID,dstID,data_len,type_,extype,cmd_data_ack)
	return headAndType
