from model import Status
class RequestReceived:
	def __init__(self, message, status, timeout):
		self.message : str = message
		self.status : Status = status
		self.timeout : int = timeout

	def to_dict(self):
		return {
			"timeout": self.timeout,
			"message": self.message,
			"status": self.status.name,
		}