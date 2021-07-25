import logging
from gevent import monkey
monkey.patch_all()
from gevent.pywsgi import WSGIServer
from flask_compress import Compress

from flask import Flask, jsonify, request
import sys

from MinecraftService import MinecraftService, AlreadyRunningException, CooldownException
from Security import Security
from AppConfig import AppConfig

app = Flask(__name__)
compress = Compress()
compress.init_app(app)

minecraftService = MinecraftService.getInstance()
config = AppConfig.getInstance()

@app.route("/minecraft/ping", methods=["GET"])
def ping():
	print("Ping")
	return {"message":"Pong"}, 200

@app.route("/minecraft/start", methods=["POST"])
def start():
	auth = request.headers.get("Authorization")
	valid = Security.validateToken(auth)

	if(not valid):
		return {
			"error": "Invalid token",
			"detail": None
			}, 401

	print("Request to start")

	try:
		minecraftService.start()
		return {
			"message":"Starting the server."
			}, 200
	except (AlreadyRunningException, CooldownException) as e:
		return {
			"error":"Error starting the server.",
			"detail": str(e)
			}, 400
	except Exception as e:
		return {
			"error":"Error starting the server.",
			"detail": str(e)
			}, 500

@app.route("/minecraft/info", methods=["GET"])
def info():

	auth = request.headers.get("Authorization")
	valid = Security.validateToken(auth)

	if(not valid):
		return {
			"error": "Invalid token",
			"detail": None
			}, 401
	
	status = minecraftService.getStatus()

	if(status is None):
		return {"status": "offline"}, 200
	
	return status, 200

if(__name__ == '__main__'):

	if(len(sys.argv) > 1):
		if(sys.argv[1] == "generatetoken"):
			Security.generateToken()
			print("Token generated")
		else:
			print("Unknown argument")
	else:
		print("Starting server")
		http_server = WSGIServer((config.flaskHost, config.flaskPort), app, log="info")
		http_server.serve_forever()

		# app.run(
		# 	debug=True,
		# 	host=config.flaskHost,
		# 	port=config.flaskPort
		# )