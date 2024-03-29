import socket
import sys
import pickle

class client(object):
	def __init__(self,host,port):
		self.host = socket.gethostbyname(host)
		self.port = port
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	def comandos(self):
		print(self.host)
		probar = False
		while True:
			cmd = input(">>ingrese instrucciones\n>>")
			if cmd == "connect" and probar == False:
				intento = self.intentar_conexion()
				if intento == True:
					print("Conectado a servidor")
					probar = True
				else:
					print("No se logro conectar")
			elif cmd == "disconnect":
				if probar == True:
					mensaje = "disconnect"
					self.sock.send(mensaje.encode('utf8'))
					self.sock.close()
					probar = False
					print("Desconectado")
				else:
					print("Ya se ha desconectado o nunca estuvo conectado")
			elif cmd == "quit":
				if probar == True:
					self.sock.close()
					probar = False
					break	
				else:
					break
			elif cmd == "input kv":
				if probar == True:
					while True:
						try:
							values = input("Ingrese key value como\n Key Value\n").split()
							if len(values) == 2:
								break
						except:
							print("incorrect key value")
							continue
					mensaje ="input "+values[0]+" "+values[1]
					self.sock.send(mensaje.encode('utf8'))
					data = self.sock.recv(1024)
					print(str(data.decode('utf8')))
				else:
					print("Not connected")
			elif cmd == "input v":
				if probar == True:
					while True:
						try:
							values = str(input("Ingrese valor como\n Valor\n"))
							break
						except:
							print("incorrect value")
							continue
					mensaje ="inputv "+values
					self.sock.send(mensaje.encode('utf8'))
					data = self.sock.recv(1024)
					print(str(data.decode('utf8')))
				else:
					print("Not connected")
			elif cmd == "get":
				if probar == True:
					while True:
						try:
							values = str(input("Ingrese clave para obtener valor\n"))
							break
						except:
							print("incorrect key")
							continue
					mensaje ="get "+values
					self.sock.send(mensaje.encode('utf8'))
					data = self.sock.recv(1024)
					print("("+values+","+str(data.decode('utf8'))+")")
				else:
					print("Not connected")
			elif cmd == "update":
				if probar == True:
					while True:
						try:
							key_new_value = input("Ingrese key y nuevo valor como\n Key Value\n").split()
							if len(values) == 2:
								break
							if key_new_value[0] == " " or key_new_value[1] == " ":
								continue
						except:
							print("incorrect key value")
							continue
					mensaje ="update "+key_new_value[0]+" "+key_new_value[1]
					self.sock.send(mensaje.encode('utf8'))
					data = self.sock.recv(1024)
					print(str(data.decode('utf8')))
				else:
					print("not connected")
			elif cmd == "delete":
				if probar == True:
					while True:
						try:
							key = str(input("Ingrese key  como\n Key \n"))
							break
						except:
							print("incorrect key value")
							continue
					mensaje ="delete "+key
					self.sock.send(mensaje.encode('utf8'))
					data = self.sock.recv(1024)
					print(str(data.decode('utf8')))
				else:
					print("not connected")
			elif cmd == "list":
				if probar == True:
					mensaje = "list key"
					self.sock.send(mensaje.encode('utf-8'))
					data = self.sock.recv(1024)
					temp_a = pickle.loads(data)
					print(temp_a)
				else:
					print("Not connected")
	def intentar_conexion(self):#maneja la conexion si se ingresa comando connect
		try:
			self.sock.connect((self.host,self.port))
			return True
		except:
			return False
			

if __name__ == "__main__":
	while True:
		port_num = input("port?\n>>")
		try:
			port_num = int(port_num)
			break
		except ValueError:
			pass
	host_ip = input("Host IP?\n>>")
	client(host_ip,port_num).comandos()
