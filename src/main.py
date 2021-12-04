import logging
import sys

# from flask import app, config
from gevent import monkey
monkey.patch_all()
from gevent.pywsgi import WSGIServer

from core import AppConfig, Security
# from API import app
from controllers.Minecraft import app

logger = logging.getLogger(__name__)
config = AppConfig.getInstance()

if(__name__ == '__main__'):

	# Generate a token
	if(len(sys.argv) > 1):
		if(sys.argv[1] == "generatetoken"):
			Security.generateToken()
			logger.info("Token generated")
		else:
			logger.info("Unknown argument")
			
	else:
		logger.info("Starting flask server...")
		http_server = WSGIServer((config.flaskHost, config.flaskPort), app)
		logger.info(f"Listening on {config.flaskHost}:{config.flaskPort}")
		http_server.serve_forever()

		# app.run(
		# 	debug=True,
		# 	host=config.flaskHost,
		# 	port=config.flaskPort
		# )