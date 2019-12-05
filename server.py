import socket
import threading

class server(object):
	def __init__(self,host,port):
		self.host = host
		self.port = port
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.bind((self.host,self.port))
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
				data = client.recv(size)
				if data:
					response = data
					client.send(response)
				else:
					raise error('Client disconnected')
			except:
				client.close()
				return False
if __name__ == "__main__":
	while True:
		port_num = input("port?")
		try:
			port_num = int(port_num)
			break
		except ValueError:
			pass
	#try:
	server('',port_num).listen()
	#except:
		#print("Permiso denegado\nPuerto no permitido\n")
