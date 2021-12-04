from gevent import monkey
monkey.patch_all()

import logging
import sys

from flask_compress import Compress
from flask import Flask, jsonify, request
from flask.logging import default_handler

from service.MinecraftService import MinecraftService, AlreadyRunningException
# from Security import Security
from core import AppConfig, Security

app = Flask(__name__)
app.logger.removeHandler(default_handler)
compress = Compress()
compress.init_app(app)

handler = logging.StreamHandler(sys.stdout)
logging.basicConfig(level=logging.INFO, handlers=[handler])
logger = logging.getLogger(__name__)

minecraftService = MinecraftService.getInstance()
config = AppConfig.getInstance()

def errorWrapper(e: Exception, msg=None):
	return {
		"type": e.__class__.__name__,
		"detail": str(e),
		"error": msg
	}

@app.route("/minecraft/ping", methods=["GET"])
def ping():
	logger.info("ping")
	return {"message":"Pong"}, 200

@app.route("/minecraft/start", methods=["POST"])
def start():
	auth = request.headers.get("Authorization")
	valid = Security.validateToken(auth)

	if(not valid):
		return {
			"type": "InvalidToken",
			"error": "Invalid token",
			"detail": None
			}, 401

	logger.info("Request to start")

	try:
		minecraftService.start()
		return {"message":"Starting the server."}, 200

	except AlreadyRunningException as e:
		return errorWrapper(e, "Error starting the server."), 400
	except Exception as e:
		return errorWrapper(e, "Error starting the server."), 500

@app.route("/minecraft/info", methods=["GET"])
def info():
	auth = request.headers.get("Authorization")
	valid = Security.validateToken(auth)

	if(not valid):
		return {
			"type": "InvalidToken",
			"error": "Invalid token",
			"detail": None
			}, 401
	
	status = minecraftService.getStatus()

	if(status is None):
		return {"status": "offline"}, 503
	
	return status, 200