from datetime import datetime, timedelta
import subprocess
import logging
import sys

from mcstatus import MinecraftServer

from AppConfig import AppConfig

handler = logging.StreamHandler(sys.stdout)
logging.basicConfig(level=logging.INFO, handlers=[handler])
logger = logging.getLogger(__name__)

config = AppConfig.getInstance()

class AlreadyRunningException(Exception): pass

class MinecraftService:

	_instance = None

	def __init__(self):

		self._serverProcess = None

	@classmethod
	def getInstance(cls):
		if(cls._instance is None):
			cls._instance = MinecraftService()
		return cls._instance

	def getStatus(self):
		try:
			address = config.minecraftServerHost + ":" + config.minecraftServerPort
			server = MinecraftServer.lookup(address)
			status = server.status()
		except Exception:  # most likely unable to connect, meaning server unavaillable
			return None

		return status.raw

	def isRunning(self):
		if(self._serverProcess == None):
			return False

		# check if process has terminated
		poll = self._serverProcess.poll()
		if(poll == None):
			return True
		else:
			return False

	def start(self):
		if(self.isRunning()):
			raise AlreadyRunningException("Sever already running.")

		logger.info("Starting the minecraft server...")
		
		self._runServer()

	def _runServer(self):
		self._serverProcess = subprocess.Popen(
			config.minecraftServerCommand.split(),
			shell=True,
			cwd=config.minecraftServerPath,
			# stdout=subprocess.DEVNULL,
			# stderr=subprocess.DEVNULL,
		)