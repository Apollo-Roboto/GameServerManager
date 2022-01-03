import subprocess
import signal
import logging
import re
from threading import Thread, Event
import threading

from core import AppConfig

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

		self.on_ready_events = []
		self.on_exit_events = []
		self.on_reminder_events = []
		self.on_start_timeout = []
		self.on_ready_events.append(self.reset_server_timeout) # starts the timeout to kill the server
		self.on_start_timeout.append(self.stop) # tries to stops the server

	def run(self):
		self.proc = subprocess.Popen(
			self.cmd,
			cwd=self.cwd,
			stdout=subprocess.PIPE,
			stderr=subprocess.STDOUT
		)

		# Starting the timeout timer will call the stop method later. if not canceled
		self._start_timeout_timer(self.start_timeout)
		
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
				self._cancel_timeout_timer()
				logger.info("Stopped listening for readyLog")

		logger.info("Waiting for process to stop...")
		self.proc.wait()
		logger.info(f"Process done with exit code {self.proc.poll()}")
		self._on_exit()

	def stop(self):
		# stop the autostop
		self.stoping_event.set()

		# stop the process
		self.proc.send_signal(signal.SIGTERM)

	def reset_server_timeout(self):
		s = config.serverTimeout
		reminder_time = config.reminderTime
		
		if(self._auto_stop_thread is not None and self._auto_stop_thread.is_alive):
			logger.info("Auto stop thread was already running, reseting to extend timeout...")

			# set will tell the thread to skip the timout and terminate
			self.stoping_event.set()

		def func():
			logger.info(f"Stopping the thread in {s} seconds.")

			# wait for reminderTime
			# Flag will be true if request to reset has been called
			flag = self.stoping_event.wait(reminder_time)
			if(not flag):
				logger.info(f"Reminder time reached.")
				self._on_reminder(s - reminder_time)

			# Flag will be true if request to reset has been called
			flag = self.stoping_event.wait(s - reminder_time)

			# If flag is false, timeout was reached
			if(not flag):
				logger.info(f"Auto stop time reached, stopping the thread...")
				self.stop()

		self._auto_stop_thread = Thread(target=func)
		self.stoping_event.clear() # flag needs to be cleared
		self._auto_stop_thread.start()

	def _start_timeout_timer(self, timeout):
		if(self.timeout_timer is None or not self.timeout_timer.is_alive()):
			logger.info("Starting the timeout_timer thread.")
			self.timeout_timer = threading.Timer(timeout, self._on_start_timeout)
			self.timeout_timer.start()

	def _cancel_timeout_timer(self):
		logger.info("Stopping the timeout_timer thread.")
		self.timeout_timer.cancel()

	def _on_start_timeout(self):
		logger.info("Calling on_start_timeout")
		for event in self.on_start_timeout:
			event()

	def _on_ready(self):
		logger.info("Calling on_ready_events")
		for event in self.on_ready_events:
			event()
	
	def _on_exit(self):
		logger.info("Calling on_exit_events")
		for event in self.on_exit_events:
			event()

	def _on_reminder(self, timeLeft):
		logger.info("Calling on_reminder_events")
		for event in self.on_reminder_events:
			event(timeLeft)