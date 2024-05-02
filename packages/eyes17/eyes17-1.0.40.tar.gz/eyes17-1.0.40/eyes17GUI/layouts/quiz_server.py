from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication

# blueprint for socket comms parts of app
flask_thread = None
showStatusSignal = None
import socket

def setStatusSignal(sig):
	global showStatusSignal
	showStatusSignal = sig

def create_server(showStatusSignal, serverSignal, local_ip):
	setStatusSignal(showStatusSignal)
	flask_thread = QuizResponseThread()
	flask_thread.setServerSignal(serverSignal)
	# flask_thread.finished.connect(QApplication.quit)
	# Start the thread
	flask_thread.start()
	return flask_thread

class QuizResponseThread(QThread):
	finished = pyqtSignal()
	serverSignal = None

	def setServerSignal(self, sig):
		self.serverSignal = sig

	def run(self):
		self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.serversocket.bind(('0.0.0.0', 4000))
		self.serversocket.listen(50)  # become a server socket, maximum 50 connections
		while True:
			connection, address = self.serversocket.accept()
			buf = connection.recv(64)
			if len(buf) > 0:
				print(address, buf)
				self.serverSignal.emit(str(address[0]),buf.decode('utf-8'))