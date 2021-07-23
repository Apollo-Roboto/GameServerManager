from flask import Flask, jsonify, request
import sys

from MinecraftService import MinecraftService
from Security import Security
from AppConfig import AppConfig

app = Flask(__name__)

minecraftService = MinecraftService.getInstance()

@app.route("/minecraft/ping", methods=["GET"])
def ping():
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

	try:
		minecraftService.start()
		return {
			"message":"Starting the server."
			}, 200

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
		app.run(
			debug=True,
			host="0.0.0.0",
			port=AppConfig.getInstance().port
		)