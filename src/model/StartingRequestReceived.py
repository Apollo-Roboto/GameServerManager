from dataclasses import dataclass

@dataclass
class StartingRequestReceived:
	message : str
	timeout : int