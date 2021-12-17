import logging
import sys
import requests
from threading import Thread

from core import AppConfig, ProcessHandler
from model import RequestResult, Status, Game

handler = logging.StreamHandler(sys.stdout)
logging.basicConfig(level=logging.INFO, handlers=[handler])
logger = logging.getLogger(__name__)

config = AppConfig.getInstance()



class AlreadyRunningException(Exception): pass
class NotRunningException(Exception): pass



class ServerService:
	_instance = None

	def __init__(self):
		self._thread : ProcessHandler = None
	
	@classmethod
	def getInstance(cls):
		if(cls._instance is None):
			cls._instance = ServerService()
		return cls._instance

	def is_running(self):
		if(self._thread == None):
			return False

		if(self._thread.proc == None):
			return False

		# check if process has terminated
		poll = self._thread.proc.poll()
		if(poll == None):
			return True
		else:
			return False

	def start(self, game: Game, callback_url=None):
		if(self.is_running()):
			raise AlreadyRunningException()
	
		logger.info(f"Starting the server... workingDirectory: '{game.path}', command: '{game.command}'")

		self._thread = ProcessHandler(
			cmd=game.command.split(),
			cwd=game.path,
			ready_log=game.ready_log,
			timeout=game.timeout
		)
		if(callback_url is not None):
			self._thread.on_ready_events.append(ServerService._on_ready_factory(callback_url))
			self._thread.on_exit_events.append(ServerService._on_exit_factory(callback_url))
		self._thread.start()

	def stop(self):
		if(not self.is_running()):
			raise NotRunningException()
		
		self._thread.stop()

	def reset_timeout(self):
		if(self.is_running()):
			self._thread.reset_timeout()
		else:
			logger.info("Tried to reset timeout but no thread was running.")

	def _on_ready_factory(callback_url):
		"""Factory so I can create a function with the callBack more easily"""
		def on_ready():
			logger.info(f"Server is ready, calling '{callback_url}'")
			result = RequestResult(
				message="Server has started.",
				status=Status.RUNNING,
				details=None
			)

			def do_the_callback():
				try:
					response = requests.post(callback_url, json=result.to_dict())
					if(response.status_code == 200):
						logger.info(f"Successfully called {callback_url}.")
					else:
						logger.info(f"Failed to call {callback_url}. Received {response.status_code}.")
				except requests.exceptions.ConnectionError as e:
					logger.info(f"Connection error with {callback_url}. {e}")
			
			Thread(target=do_the_callback).start()
		return on_ready

	def _on_exit_factory(callback_url):
		"""Factory so I can create a function with the callBack more easily"""
		def on_exit():
			logger.info(f"Server has stopped, calling '{callback_url}'")
			result = RequestResult(
				message="Server has stopped.",
				status=Status.STOPPED,
				details=None
			)

			def do_the_callback():
				try:
					response = requests.post(callback_url, json=result.to_dict())
					if(response.status_code == 200):
						logger.info(f"Successfully called {callback_url}.")
					else:
						logger.info(f"Failed to call {callback_url}. Received {response.status_code}.")
				except requests.exceptions.ConnectionError as e:
					logger.info(f"Connection error with {callback_url}. {e}")
			
			Thread(target=do_the_callback).start()
		return on_exit
