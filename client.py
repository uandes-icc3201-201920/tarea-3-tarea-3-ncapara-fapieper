import socket
import sys

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
					#hacer desconexion
					print("manejar desconexion")
				else:
					print("Ya se ha desconectado o nunca estuvo conectado")
			elif cmd == "quit":
				if probar == True:
					#manejar el quit
					print("manejar el quit")
				else:
					break
	def intentar_conexion(self):
		try:
			self.sock.connect((self.host,self.port))
			return True
		except:
			return False
			

if __name__ == "__main__":
	client('',12534).comandos()
