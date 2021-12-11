class Error:
	def __init__(self, message, details):
		self.message : str = message
		self.details : str = details

	def to_dict(self):
		return {
			"details": self.details,
			"message": self.message,
		}