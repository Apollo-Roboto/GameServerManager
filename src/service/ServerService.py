import logging
import sys
import requests
from threading import Thread

from core import AppConfig, ProcessHandler, Webhook
from model import Game, WebhookData

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
			start_timeout=game.timeout,
		)
		
		# Sets the webhook events if present in the request
		if(callback_url is not None):
			self._thread.on_ready_events.append(lambda : Webhook.send(callback_url, WebhookData("Server has started.")))
			self._thread.on_exit_events.append(lambda : Webhook.send(callback_url, WebhookData("Server has stopped.")))
			self._thread.on_reminder_events.append(lambda x: Webhook.send(callback_url, WebhookData(f"Reminder, the server will stop in {x} seconds.")))
			self._thread.timer_start_timeout.events.append(lambda : Webhook.send(callback_url, WebhookData("Server failed to start, timeout reached.")))

		self._thread.start()

	def stop(self):
		if(not self.is_running()):
			logger.info("Tried to stop the thread but no thread was running.")
			raise NotRunningException()
		
		self._thread.stop()

	def reset_timeout(self):
		if(not self.is_running()):
			logger.info("Tried to reset timeout but no thread was running.")
			raise NotRunningException()

		self._thread.reset_server_timeout()