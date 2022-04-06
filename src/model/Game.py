import logging
from dataclasses import dataclass

from core import AppConfig

config = AppConfig.getInstance()

@dataclass
class Game:
	name: str
	version: str
	path: str
	command: str
	ready_log: str
	timeout: str
	enabled: bool

	@classmethod
	def get_game(cls, name, version=None):

		# get capitalized name (makes case insensitive)
		for game in config.games.keys():
			if(game.lower() == name.lower()):
				name = game
				break

		if(name not in config.games):
			raise ValueError("Game not found")

		game_config = config.games[name]

		if(version is not None and "versions" not in game_config):
			raise ValueError("This game does not have alternative versions.")

		# get capitalized version (makes case insensitive)
		if(version is not None):
			for game_version in game_config["versions"].keys():
				if(game_version.lower() == version.lower()):
					version = game_version
					break

		if("versions" in config.games[name]):

			# if there are version listed and no version specified
			if(version is None and "default" not in game_config):
				raise ValueError(f"The game '{name}' does not have a default version.")
			
			# set the default version if version is none
			if(version is None):
				version = game_config["default"]

			# if version specified does not exist
			if(version not in game_config["versions"]):
				raise ValueError(f"Version '{version}' not found for '{name}'.")

		if(version is not None):
			path = game_config["versions"][version]["path"]
			command = game_config["versions"][version]["command"]
			ready_log = game_config["versions"][version]["readyLog"]
			timeout = game_config["versions"][version]["timeout"]
			if("enabled" in game_config["versions"][version]):
				enabled = game_config["versions"][version]["enabled"]
			else:
				enabled = True
		else:
			path = game_config["path"]
			command = game_config["command"]
			ready_log = game_config["readyLog"]
			timeout = game_config["timeout"]
			if("enabled" in game_config):
				enabled = game_config["enabled"]
			else:
				enabled = True

		return Game(
			name=name,
			version=version,
			path=path,
			command=command,
			ready_log=ready_log,
			timeout=timeout,
			enabled=enabled
		)