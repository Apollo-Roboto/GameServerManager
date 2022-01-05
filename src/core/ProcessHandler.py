import subprocess
import signal
import logging
import re
from threading import Thread, Event
import threading

from core import AppConfig
from core.TimedEvent import TimedEvent

logger = logging.getLogger(__name__)

config = AppConfig.getInstance()

class ProcessHandler(Thread):
	def __init__(self, cmd, cwd, ready_log, start_timeout):
		Thread.__init__(self)

		self.cmd = cmd
		self.cwd = cwd
		self.ready_log = ready_log
		self.start_timeout = start_timeout

		self._pattern = re.compile(ready_log, re.IGNORECASE)
		self._listen_for_ready = True

		self.proc : subprocess.Popen= None
		self._auto_stop_thread : Thread = None
		self.stoping_event : Event = Event()
		
		self.timeout_timer = None

		# Events
		self.on_exit_events = []
		self.on_reminder_events = []
		self.on_ready_events = []
		self.on_ready_events.append(self.reset_server_timeout) # starts the timeout to kill the server

		self.timer_start_timeout = TimedEvent(start_timeout)
		self.timer_start_timeout.events.append(self.stop) # tries to stops the server when starts fails

		self.timer_reminder = TimedEvent(config.reminderTime)
		self.timer_reminder.events.append(self._on_reminder) # add the reminder event thing

		self.timer_stop = TimedEvent(config.serverTimeout)
		self.timer_stop.events.append(self.stop) # stops the server when it's time for bed

	def run(self):
		self.proc = subprocess.Popen(
			self.cmd,
			cwd=self.cwd,
			stdout=subprocess.PIPE,
			stderr=subprocess.STDOUT
		)

		# Starting the timeout timer will call the stop method later. if not canceled
		self.timer_start_timeout.start()
		
		# printing and scanning each line comming out of the process
		for line in self.proc.stdout:
			s = str(line, encoding="utf-8").rstrip()
			print(s)

			if(not self._listen_for_ready):
				continue

			# checking for the ready log
			if(self._pattern.search(s)):
				self._on_ready()
				self._listen_for_ready = False
				self.timer_start_timeout.cancel()
				logger.info("Stopped listening for readyLog")

		self.timer_reminder.cancel()
		logger.info("Waiting for process to stop...")
		self.proc.wait()
		logger.info(f"Process done with exit code {self.proc.poll()}")
		self._on_exit()

	def stop(self):
		# stop the process
		self.proc.send_signal(signal.SIGTERM)

		# stops the timers
		self.timer_start_timeout.cancel()
		self.timer_stop.cancel()
		self.timer_reminder.cancel()

	def reset_server_timeout(self):
		"""Resets the auto stop timer to allow more time on the server if needed"""
		# calling start() resets the TimedEvents
		self.timer_stop.start() 
		self.timer_reminder.start()

	def _on_ready(self):
		logger.info("Calling on_ready_events")
		for event in self.on_ready_events:
			event()
	
	def _on_exit(self):
		logger.info("Calling on_exit_events")
		for event in self.on_exit_events:
			event()

	def _on_reminder(self):
		time_left = config.serverTimeout - config.reminderTime
		logger.info(f"Calling on_reminder_events, time left: {time_left}")
		for event in self.on_reminder_events:
			event(time_left)