import struct

def drop_msg():
	ptl_ID = 0
	gateway_do = 0
	prio = 0
	ndst = 1
	srcID = b'\x12\x23\x34\x45\x56\x67\x11\x22'
	dstID = b'\x00\x00\x00\x00\x00\x00\x00\x00'
	data_len = 8
	type_ = 0xfffe
	extype = 0x03020102
	packet = struct.pack('4B8s8shHi',ptl_ID, gateway_do, prio, ndst, srcID, dstID, data_len,type_,extype)
	total_len = struct.pack('i',len(packet))
	return total_len+packet

print(drop_msg())
