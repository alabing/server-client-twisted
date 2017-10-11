import sys, os, struct, time
from header import MsgHeader, HeadAndType
import function, protocol, header

class doMsg:
	def __init__(self):
		self.msg_buf = b''

	def msg_manage(self,msg,node,thisNode):
		self.msg_buf += msg
		while True:
			total_len, = struct.unpack('i',self.msg_buf[:4])
			if total_len > len(self.msg_buf)-4:
				break
			packet = self.msg_buf[:total_len+4]
			headAndType = header.getHeadAndType(packet)
			self.packet_manage(packet,headAndType,node,thisNode)
			self.msg_buf = self.msg_buf[total_len+4:]
			if len(self.msg_buf) < 26:
				break

	def packet_manage(self,packet,headAndType,node,thisNode):
		if headAndType.cmd_data_ack == protocol.ACK:
			pass
		else:   #DATA
			if headAndType.extype == protocol.ATTRIBUTE:
				thisNode.attPackage = packet
				thisNode.nodeID = headAndType.srcID
				node.broadcast(packet)
				mac = function.mac2str(headAndType.srcID)
				print(mac)
				charactor = header.getCharactor(packet,headAndType.ndst)
			elif headAndType.extype == protocol.HEART_BEAT:
				thisNode.heartbeat_time = int(time.time())
			elif headAndType.extype == protocol.ERROR:
				node.broadcast(packet)
			elif headAndType.extype == protocol.SCAN_SINGLE:
				node.send_spec(packet)
				print('send singleMsg, time = ',end='')
				print(time.time())
			else:
				pass

	def cmd_manage(self,node,msg,thisNode):
		headAndType = header.getHeadAndType(msg)
		if headAndType.extype == protocol.SCAN_SINGLE:
			node.start_spec(headAndType.dstID,msg,thisNode)
		elif headAndType.extype == protocol.STOP_CMD:
			taskIndex = msg.index(b'taskextype=')
			print(msg[taskIndex+len(b'taskextype='):taskIndex+len(b'taskextype=')+4])
			taskextype, = struct.unpack('i', msg[taskIndex+len(b'taskextype='):taskIndex+len(b'taskextype=')+4])
			if taskextype == protocol.SCAN_SINGLE:
				node.stop_spec(headAndType.dstID,msg,thisNode)
			else:
				pass
		elif headAndType.extype == protocol.RESET:
			node.trans_cmd(headAndType.dstID,msg,thisNode)
		elif headAndType.extype == protocol.REMOVE:
			node.trans_cmd(headAndType.dstID,msg,thisNode)
		elif headAndType.extype == protocol.MODIFYAP:
			node.trans_cmd(headAndType.dstID,msg,thisNode)
		elif headAndType.extype == protocol.MODIFYIP:
			node.trans_cmd(headAndType.dstID,msg,thisNode)
		elif headAndType.extype == protocol.SLEEP:
			node.trans_cmd(headAndType.dstID,msg,thisNode)
		elif headAndType.extype == protocol.NOTIFY_NETCOMMUNITY:
			node.trans_cmd(headAndType.dstID,msg,thisNode)
		elif headAndType.extype == protocol.NOTIFY_IP:
			node.trans_cmd(headAndType.dstID,msg,thisNode)
		elif headAndType.extype == protocol.SWITCH_MODE:
			node.trans_cmd(headAndType.dstID,msg,thisNode)
		else:
			pass
