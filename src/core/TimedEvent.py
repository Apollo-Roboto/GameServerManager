import logging
from threading import Timer

logger = logging.getLogger(__name__)

class TimedEvent:
	def __init__(self, time):
		self.timer : Timer = None
		self.time = time
		self.events = []

	def start(self):
		"""Starts the timer, cancel the previous timer if it was running"""
		if(self.timer is not None and self.timer.is_alive):
			self.timer.cancel()

		self.timer = Timer(self.time, self._invoke)
		self.timer.start()
	
	def cancel(self):
		"""Cancels the timer"""
		if(self.timer is not None):
			self.timer.cancel()
	
	def _invoke(self):
		"""Invokes all the events"""
		for event in self.events:
			try:
				event()
			except:
				logger.exception(f"Failed to call event")