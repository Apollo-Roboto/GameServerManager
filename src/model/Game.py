import logging
from core import AppConfig

config = AppConfig.getInstance()

class Game:
	def __init__(self, name, version, path, command, ready_log, timeout):
		self.name = name
		self.version = version
		self.path = path
		self.command = command
		self.ready_log = ready_log
		self.timeout = timeout
	
	def to_dict(self):
		return {
			"name": self.name,
			"version": self.version,
			"path": self.path,
			"command": self.command,
			"ready_log": self.ready_log,
			"timeout": self.timeout,
		}

	@classmethod
	def get_game(cls, name, version=None):
		if(name not in config.games):
			raise ValueError("game not found")

		game_config = config.games[name]

		if("versions" in config.games[name]):

			# if there are version listed and no version specified
			if(version is None and "default" not in game_config):
				raise ValueError(f"The game '{name}' does not have a default version")
			
			# set the default version if version is none
			if(version is None):
				version = game_config["default"]

			# if version specified does not exist
			if(version not in game_config["versions"]):
				raise ValueError(f"Version '{version}' not found for '{name}'")
			
		if(version is not None):
			path = game_config["versions"][version]["path"]
		else:
			path = game_config["path"]

		if(version is not None):
			command = game_config["versions"][version]["command"]
		else:
			command = game_config["command"]

		if(version is not None):
			ready_log = game_config["versions"][version]["readyLog"]
		else:
			ready_log = game_config["readyLog"]

		if(version is not None):
			timeout = game_config["versions"][version]["timeout"]
		else:
			timeout = game_config["timeout"]

		return Game(
			name=name,
			version=version,
			path=path,
			command=command,
			ready_log=ready_log,
			timeout=timeout,
		)