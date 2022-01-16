import logging
import sys
import validators

from flask_compress import Compress
from flask import Flask, json, jsonify, request
from flask.logging import default_handler

from core import AppConfig, Security
from model import StartingRequestReceived, StopingRequestReceived, Error, Game, ResetTimeoutResponse
from service import ServerService, AlreadyRunningException, NotRunningException

app = Flask(__name__)
app.logger.removeHandler(default_handler)
compress = Compress()
compress.init_app(app)

handler = logging.StreamHandler(sys.stdout)
logging.basicConfig(level=logging.INFO, handlers=[handler])
logger = logging.getLogger(__name__)

config = AppConfig.getInstance()
serverService = ServerService.getInstance()

@app.route("/server/ping", methods=["GET"])
def ping():
	logger.info("ping")
	return {"msg":"🤖"}, 200

@app.route("/server/resetTimeout", methods=["POST"])
def reset_timeout():
	auth = request.headers.get("Authorization")
	valid = Security.validateToken(auth)

	if(not valid):
		return Error(
			message="Unauthorized",
			details="Provided token was invalid",
		).__dict__, 401

	try:
		serverService.reset_timeout()
	except NotRunningException as e:
		return Error(
			message="Bad request",
			details="No game is running",
		).__dict__, 400

	return ResetTimeoutResponse(
		server_timeout=config.serverTimeout
	).__dict__, 200

@app.route("/server/start", methods=["POST"])
def start():
	auth = request.headers.get("Authorization")
	valid = Security.validateToken(auth)

	if(not valid):
		return Error(
			message="Unauthorized",
			details="Provided token was invalid",
		).__dict__, 401
	
	if("game" not in request.args):
		return Error(
			message="Bad request",
			details="The parameter 'game' is required.",
		).__dict__, 400

	try:
		game = Game.get_game(
			name=request.args.get("game"),
			version=request.args.get("version"),
		)
	except ValueError as e:
		return Error(
			message="Bad request",
			details=str(e),
		).__dict__, 400
	
	callback_url = request.headers.get("Callback-Url")
	
	if(callback_url is not None and not validators.url(callback_url)):
		return Error(
			message="Bad request",
			details="Invalid Callback-Url",
		).__dict__, 400

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
		).__dict__, 400

	return StartingRequestReceived(
		game=game.name,
		version=game.version,
		server_timeout=config.serverTimeout,
	).__dict__, 200

@app.route("/server/stop", methods=["POST"])
def stop():
	auth = request.headers.get("Authorization")
	valid = Security.validateToken(auth)

	if(not valid):
		return Error(
			message="Unauthorized",
			details="Provided token was invalid",
		).__dict__, 401

	logger.info(f"Request to stop...")

	try:
		serverService.stop()
	except NotRunningException:
		return Error(
			message="Bad request",
			details="No game is running",
		).__dict__, 400

	return StopingRequestReceived(
		message=f"Stopping",
	).__dict__, 200

@app.route("/servers", methods=["GET"])
def list_servers():
	auth = request.headers.get("Authorization")
	valid = Security.validateToken(auth)

	if(not valid):
		return Error(
			message="Unauthorized",
			details="Provided token was invalid",
		).__dict__, 401

	new_dict = {}

	# get the games
	for game_name, game_data in config.games.items():

		new_dict[game_name] = {}

		if("versions" in game_data):
			versions = game_data["versions"].keys()
			new_dict[game_name]["versions"] = list(versions)

		if("default" in game_data):
			new_dict[game_name]["default"] = game_data["default"]

	return new_dict, 200
