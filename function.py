import protocol
import struct
import pymysql
from random import Random

def randomStr(randomlength=4):
	str = ''
	chars = '0123456789'
	length = len(chars) - 1
	random = Random()
	for i in range(randomlength):
		str+=chars[random.randint(0, length)]
	return str

namelist = []
def createName(seed):
	name = seed + "-" + randomStr()
	if name not in namelist:
		namelist.append(name)
		return name
	else:
		createName(seed)

def mac2str(mac):
	str_mac='%02x:%02x:%02x:%02x:%02x:%02x'%(mac[0],mac[1],mac[2],mac[3],mac[4],mac[5])
	return str_mac.upper()

id_num = 1
def addtoSQL(nodeCharactor):
	name = 'gateway-%04d'%id_num
	id_num += 1
	mac = mac2str(nodeCharactor.DMAC)
	db = pymysql.connect('localhost','root','123456','hbqdb')
	cursor = db.cursor()
	create_table = '''create table if not exists nodetable(
                   name varchar(20), 
                   mac varchar(20))'''
	insert_node='''INSERT INTO nodetable(name, mac) SELECT '%s'%name, '%s'%mac FROM DUAL WHERE NOT EXISTS(SELECT mac FROM nodetable
WHERE mac = '%s'%mac);'''
	db.close()
