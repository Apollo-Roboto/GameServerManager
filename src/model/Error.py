from dataclasses import dataclass

@dataclass
class Error:
	message: str
	details: str