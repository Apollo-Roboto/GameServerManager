from flask import Flask, jsonify, request
from MinecraftService import MinecraftService

app = Flask(__name__)

minecraftService = MinecraftService.getInstance()

@app.route("/minecraft/ping", methods=["GET"])
def ping():
	return {"msg":"Hello"}, 200

@app.route("/minecraft/start", methods=["POST"])
def start():

	auth = request.headers.get("authorisation")
	print(auth)

	minecraftService.start()
	return {"msg":"Hello"}, 200

@app.route("/minecraft/info", methods=["POST"])
def info():
	
	status = minecraftService.getStatus()

	if(status is None):
		return {"status": "offline"}, 200
		
	return status, 200

if(__name__ == '__main__'):
	app.run(debug=True)