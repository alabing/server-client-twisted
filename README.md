# server-client-twisted
程序执行：python server.py
服务端开8010和8020两个端口，分别用于连接客户端节点和传感器节点
客户端发送命令到服务器，服务器转发给相应传感器节点
#命令格式：“type=0xFFFE；extype=; times=;freq= ;rbw= ;ifbw= ;squ= ;dem= ; att= ;auto= ;gain= ; avertime=;”指定监测中心频率、分别率等参数
服务器奖传感器节点回传的频谱数据转发给相应的客户端，客户端生成频谱态势
