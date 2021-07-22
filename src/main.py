from flask import Flask, jsonify, request

from MinecraftService import MinecraftService
from Security import Security

app = Flask(__name__)

minecraftService = MinecraftService.getInstance()

@app.route("/minecraft/ping", methods=["GET"])
def ping():
	return {"msg":"Hello"}, 200

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
	app.run(debug=True)