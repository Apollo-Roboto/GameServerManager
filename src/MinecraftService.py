from datetime import datetime, timedelta
from os import path
import os
import logging
import subprocess
from time import sleep

from mcstatus import MinecraftServer

from AppConfig import AppConfig

logger = logging.getLogger(__name__)

class AlreadyRunningException(Exception): pass
class TooSoonException(Exception): pass

class MinecraftService:

	_instance = None

	def __init__(self):
		config = AppConfig.getInstance()
		
		self.address = config.serverAddress
		self.serverComand = config.serverCommand
		self.serverPath = config.serverPath

		# 2 minutes cooldown, to prevent starting the server twice
		self.cooldown = 2
		self._nextRetry = datetime.now()

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

		if(datetime.now() < self._nextRetry):
			raise TooSoonException("Wait for cooldown before trying to start again.")

		status = self.getStatus()
		if(status != None):
			raise AlreadyRunningException("Sever already running.")

		# set the for two minutes
		self._nextRetry = datetime.now() + timedelta(minutes=self.cooldown)
		self._runServer()

	def _runServer(self):
		subprocess.Popen(self.serverComand.split(),
			shell=True,
			stdout=subprocess.DEVNULL,
			stderr=subprocess.DEVNULL,
			cwd=self.serverPath
		)