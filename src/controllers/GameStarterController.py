import logging
from os import error
import sys
import validators

from flask_compress import Compress
from flask import Flask, json, jsonify, request
from flask.logging import default_handler

# from service.MinecraftService import MinecraftService, AlreadyRunningException
from core import AppConfig, Security
from model import RequestReceived, Error, Status, Game
from service import ServerService, AlreadyRunningException

app = Flask(__name__)
app.logger.removeHandler(default_handler)
compress = Compress()
compress.init_app(app)

handler = logging.StreamHandler(sys.stdout)
logging.basicConfig(level=logging.INFO, handlers=[handler])
logger = logging.getLogger(__name__)

config = AppConfig.getInstance()
serverService = ServerService.getInstance()

@app.route("/webhook", methods=["POST"])
def webhooktest():
	return {"msg":"received"}, 200

@app.route("/server/ping", methods=["GET"])
def ping():
	logger.info("ping")
	return {"msg":"🤖"}, 200

@app.route("/server/<game>/start", methods=["POST"])
def start(game):
	auth = request.headers.get("Authorization")
	valid = Security.validateToken(auth)

	if(not valid):
		return Error(
			message="Unauthorized",
			details="Provided token was invalid",
		).to_dict(), 401

	try:
		game = Game.get_game(
			name=game,
			version=request.args.get("version"),
		)
	except ValueError as e:
		return Error(
			message="Bad request",
			details=str(e),
		).to_dict(), 400
	
	callback_url = request.headers.get("Callback-Url")
	
	if(callback_url is not None and not validators.url(callback_url)):
		return Error(
			message="Bad request",
			details="Invalid Callback-Url",
		).to_dict(), 400

	logger.info(f"Request to start. game: '{game.name}', version: '{game.version}', callback_url: '{callback_url}'")

	try:
		serverService.start(
			game=game,
			callback_url=callback_url,
		)
	except AlreadyRunningException:
		return Error(
			message="Bad request",
			details="Game already running",
		).to_dict(), 400

	return RequestReceived(
		message=f"Starting {game.name}, version: {game.version}",
		status=Status.STARTING,
		timeout=game.timeout,
	).to_dict(), 200

@app.route("/server/<game>/stop", methods=["POST"])
def info(game):
	auth = request.headers.get("Authorization")
	valid = Security.validateToken(auth)

	if(not valid):
		return Error(
			message="Unauthorized",
			details="Provided token was invalid",
		).to_dict(), 401

	logger.info(f"Request to stop {game}")

	return RequestReceived(
		message=f"Stopping {game}",
		status=Status.RUNNING,
		details=None,
	).to_dict(), 200