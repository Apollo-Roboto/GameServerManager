from dataclasses import dataclass

@dataclass
class ResetTimeoutResponse:
	server_timeout: int
