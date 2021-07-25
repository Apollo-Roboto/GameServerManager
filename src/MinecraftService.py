from datetime import datetime, timedelta
from os import path
import os
import subprocess
import logging
from multiprocessing import Process
from time import sleep

from mcstatus import MinecraftServer

from AppConfig import AppConfig
import Utils

logger = logging.getLogger(__name__)

# def detachify(func):
# 	"""Decorate a function so that its calls are async in a detached process.

# 	Usage
# 	-----

# 	.. code::
# 			import time

# 			@detachify
# 			def f(message):
# 				time.sleep(5)
# 				print(message)

# 			f('Async and detached!!!')

# 	"""
# 	# create a process fork and run the function
# 	def forkify(*args, **kwargs):
# 		if os.fork() != 0:
# 			return
# 		func(*args, **kwargs)

# 	# wrapper to run the forkified function
# 	def wrapper(*args, **kwargs):
# 		proc = Process(target=lambda: forkify(*args, **kwargs))
# 		proc.start()
# 		proc.join()
# 		return

# 	return wrapper

config = AppConfig.getInstance()

class AlreadyRunningException(Exception): pass
class CooldownException(Exception): pass

class MinecraftService:

	_instance = None

	def __init__(self):
		
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
			address = config.minecraftServerHost + ":" + config.minecraftServerPort
			server = MinecraftServer.lookup(address)
			status = server.status()
		except Exception:  # most likely unable to connect, meaning server unavaillable
			return None

		return status.raw

	def isRunning(self):
		return Utils.isPortUsed(config.minecraftServerPort)

	def start(self):
		if(datetime.now() < self._nextRetry):
			raise CooldownException("Wait for cooldown before trying to start again.")

		if(self.isRunning()):
			raise AlreadyRunningException("Sever already running.")

		print("Starting the server")

		# set the countdown
		self._nextRetry = datetime.now() + timedelta(minutes=self.cooldown)
		
		self._runServer()

	# @detachify
	def _runServer(self):
		subprocess.Popen(config.minecraftServerCommand.split(),
			shell=True,
			# stdout=subprocess.DEVNULL,
			# stderr=subprocess.DEVNULL,
			cwd=config.minecraftServerPath
		)