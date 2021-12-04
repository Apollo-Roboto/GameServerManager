import secrets
import logging
import sys

handler = logging.StreamHandler(sys.stdout)
logging.basicConfig(level=logging.INFO, handlers=[handler])
logger = logging.getLogger(__name__)

class Security:

	@classmethod
	def generateToken(cls):
		token = secrets.token_urlsafe(32)
		with open("./token", "w", encoding="utf-8") as f:
			f.write(token)

	@classmethod
	def validateToken(cls, tokenToCheck):

		if(tokenToCheck == None):
			raise Exception("token cannot be None")
		
		tokenToCheck = tokenToCheck.removeprefix("Bearer ")

		token = None
		with open("./token", "r", encoding="utf-8") as f:
			token = f.read()

		if(token is None):
			raise Exception("token not loaded")
		
		return token == tokenToCheck