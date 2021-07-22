from os import path

from mcstatus import MinecraftServer

from AppConfig import AppConfig


class MinecraftService:

	_instance = None

	def __init__(self):
		config = AppConfig.getInstance()
		self.address = "74.58.53.48:25565"
		self.serverPath = "/tmp/server"
		self.startFile = "start.sh"

	@classmethod
	def getInstance(cls):
		if(cls._instance is None):
			cls._instance = MinecraftService()
		return cls._instance

	def getStatus(self):
		try:
			server = MinecraftServer.lookup(self.address)
			status = server.status()
		except Exception:  # most likely unable to connect, meaning server unavaillable
			return None

		return status.raw

	def start(self):

		status = self.getStatus()
		if(status != None):
			raise Exception("Sever already running.")

		pass
