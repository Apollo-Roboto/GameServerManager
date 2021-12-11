from model import Status
class RequestResult:
	def __init__(self, message, status, details):
		self.message : str = message
		self.status : Status = status
		self.details : str = details

	def to_dict(self):
		return {
			"details": self.details,
			"message": self.message,
			"status": self.status.name,
		}