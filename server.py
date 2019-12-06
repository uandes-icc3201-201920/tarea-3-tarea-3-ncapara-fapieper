import socket
import threading
import random

dbLOCK = threading.Lock()

class server(object):
	def __init__(self,host,port):
		self.host = host
		self.port = port
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.bind((self.host,self.port))
		self.the_db = {}
		self.rand_key = random.randint(1000,10000)
	def listen(self):
		print("socket binded to port", self.port)
		print("host",socket.gethostbyname(self.host))
		self.sock.listen(5)
		while True:
			client, address = self.sock.accept()
			client.settimeout(600)
			threading.Thread(target = self.listenToClient, args = (client,address)).start()
	def listenToClient(self,client,address):
		size = 1024
		print('Connected to :', address)
		while True:
			try:
				data = client.recv(size)#datas como bytes  b'algo'
				if data:
					response = data
					#client.send(response)
					
					comando = response.split()
					if comando[0] == b'input':
						self.update_db_with_kv(comando,client,address)
					elif comando[0] == b'inputv':
						self.update_db_with_random_kv(comando,client,address)
					elif comando[0] == b'get':
						self.fetch_key_value(comando,client,address)
					elif comando[0] == b'update':
						self.update_key_value(comando,client,address)
					elif comando[0] == b'disconnect':
						self.try_diconnect(comando,client,address)
					elif comando[0] == b'delete':
						self.delete_key(comando,client,address)
					print(self.the_db)
				else:
					raise error('Client disconnected')
			except:
				client.close()
				return False
	def try_diconnect(self,comandos,client,address):
		client.close()
		return False
	def update_db_with_kv(self,comando,client,address):#para cuando nos dan key y values
		search_key = comando[1] in self.the_db
		if search_key == False:
			dbLOCK.acquire()
			self.the_db[comando[1]] = comando[2]
			dbLOCK.release()
			info = "Key and value added"
			client.send(info.encode('utf8'))
		else:
			info = "Key already exists"
			client.send(info.encode('utf8'))
	def update_db_with_random_kv(self,comando,client,address):#con keys al azar
		temporal = str(self.rand_key)
		tem_bytes = temporal.encode('utf-8')
		dbLOCK.acquire()
		self.the_db[tem_bytes] = comando[1]
		dbLOCK.release()
		info = "value added"
		client.send(info.encode('utf-8'))
		self.rand_key += 1
	def fetch_key_value(self,comando,client,address):#funcion para obtener el value
		search_key = comando[1] in self.the_db
		print(search_key)
		if search_key == True:
			get = self.the_db[comando[1]]
			client.send(get)
		else:
			info = "not found"
			client.send(info.encode('utf-8'))
	def update_key_value(self,comando,client,address):
		search_key = comando[1] in self.the_db
		if search_key == True:
			dbLOCK.acquire()
			self.the_db[comando[1]] = comando[2]
			dbLOCK.release()
			info = "new value updated"
			client.send(info.encode('utf-8'))
		else:
			info = "Key not found"
			client.send(info.encode('utf-8'))
	def delete_key(self,comando,client,address):
		search_key = comando[1] in self.the_db
		if search_key == True:
			dbLOCK.acquire()
			self.the_db.pop(comando[1])
			dbLOCK.release()
			info = "key deleted"
			client.send(info.encode('utf-8'))
		else:
			info = "key not found, can't delete"
			client.send(info.encode('utf-8'))
if __name__ == "__main__":
	while True:
		port_num = input("port?")
		try:
			port_num = int(port_num)
			break
		except ValueError:
			pass
	#getting host ip, name
	try:
		host_name = socket.gethostname()
		host_ip = socket.gethostbyname(host_name)
		print("Hostname: ",host_name)
		print("IP: ",host_ip)
	except:
		print("unable to get hsot ip, name")
	server('',port_num).listen()
