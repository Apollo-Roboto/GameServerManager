from dataclasses import dataclass

@dataclass
class StartingRequestReceived:
	game : str
	version : str
	server_timeout : int