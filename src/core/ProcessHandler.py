import subprocess
import logging
import re
from threading import Thread

logger = logging.getLogger(__name__)

class ProcessHandler(Thread):
	def __init__(self, cmd, cwd, ready_log, timeout):
		Thread.__init__(self)
		self.on_ready_events = []
		self.on_exit_events = []
		self.cmd = cmd
		self.cwd = cwd
		self.ready_log = ready_log
		self.timeout = timeout
		self._pattern = re.compile(ready_log, re.IGNORECASE)
		self._listen_for_ready = True
		self.proc = None

	def run(self):
		self.proc : subprocess.Popen = subprocess.Popen(
			self.cmd,
			cwd=self.cwd,
			stdout=subprocess.PIPE,
			stderr=subprocess.STDOUT
		)
		# printing and scanning each line comming out of the process
		for line in self.proc.stdout:
			s = str(line, encoding="utf-8").rstrip()
			print(s)

			# checking for the ready log
			if(self._listen_for_ready and self._pattern.search(s)):
				self._on_ready()
				self._listen_for_ready = False
				logger.info("Stopped listening for readyLog")

		logger.info("Waiting for process to stop...")
		self.proc.wait()
		logger.info(f"Process done with exit code {self.proc.poll()}")
		self._on_exit()

	def _on_ready(self):
		logger.info("Calling on_ready_events")
		for event in self.on_ready_events:
			event()
	
	def _on_exit(self):
		logger.info("Calling on_exit_events")
		for event in self.on_exit_events:
			event()
