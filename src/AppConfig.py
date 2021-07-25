import os
import logging
import json

logger = logging.getLogger(__name__)

class AppConfig:

	_instance = None

	def __init__(self):
		self._configPath = "config.json"
		self._config = {}
		self._load()

	@classmethod
	def getInstance(cls):
		if(cls._instance is None):
			cls._instance = AppConfig()
		return cls._instance

	def _load(self):
		configPath = self._configPath

		# use the default if the setting file don't exist
		if(not os.path.isfile(configPath)):
			logger.error("Could not find and load " + configPath)
			raise IOError("Could not find and load " + configPath)

		logger.info("Loading configurations from " + configPath)
		with open(configPath, "r") as f:
			try:
				jsonObj = json.load(f)
				self._config = jsonObj
				self._setProperties(self._config)
				logger.info("Loading configurations done")
			except Exception as e:
				logger.error("Loading configurations failed")
				raise e

	def _setProperties(self, properties: dict):
		for key, val in properties.items():
			setattr(self, key, val)