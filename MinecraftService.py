from mcstatus import MinecraftServer


class MinecraftService:

	address = "74.58.53.48:25565"

	_instance = None

	def __init__(self):
		pass

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
		pass
