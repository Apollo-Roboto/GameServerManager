import validators
import logging
import requests
from threading import Thread

from model import WebhookData

logger = logging.getLogger(__name__)

class Webhook:

	@classmethod
	def send(cls, url: str, data: WebhookData):
		"""Sends a webhook to a specified url with some data in a non blocking thread"""

		if(validators.url(url) != True):
			raise ValueError(f"Invalid url, got {url}")

		def do_the_webhook():
			logger.info(f"Sending webhook to '{url}', data: {data.__dict__}")
			try:
				response = requests.post(url, json=data.__dict__)
				if(response.status_code == 200):
					logger.info(f"Webhook successfully send to '{url}'.")
				else:
					logger.error(f"Webhook failed to contact '{url}'. Received {response.status_code}.")
			except requests.exceptions.ConnectionError as e:
				logger.error(f"Webhook connection error with '{url}'. {e}")
			except Exception as e:
				logger.error(f"Something wrong happened with the webhook call to '{url}'. {e}")

		Thread(target=do_the_webhook).start()