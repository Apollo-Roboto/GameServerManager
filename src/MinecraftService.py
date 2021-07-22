from os import path
import os
import logging
from flask import config

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
		logger.info("This is where I would start the server, if I was properly setup!")
		logger.info("command: " + self.serverComand)
		# os.system(cmd)
