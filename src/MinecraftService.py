from os import path
import os
import logging
import subprocess
from time import sleep

from mcstatus import MinecraftServer

from AppConfig import AppConfig

logger = logging.getLogger(__name__)

class MinecraftService:

	_instance = None

	def __init__(self):
		config = AppConfig.getInstance()
		
		self.address = config.serverAddress
		self.serverComand = config.serverCommand

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

		self._runServer()

	def _runServer(self):
		subprocess.Popen(self.serverComand.split(),
			shell=True,
			stdout=subprocess.DEVNULL,
			stderr=subprocess.DEVNULL
		)