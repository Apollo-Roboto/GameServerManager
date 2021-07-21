from flask import Flask, jsonify, request
from MinecraftService import MinecraftService

app = Flask(__name__)

minecraftService = MinecraftService.getInstance()

@app.route("/minecraft/start", methods=["POST"])
def start():
	minecraftService.start()
	return {"msg":"Hello World!"}, 200

@app.route("/minecraft/info", methods=["POST"])
def info():

	status = minecraftService.getStatus()

	if(status is None):
		return {"status": "offline"}, 200
		
	return status, 200

if(__name__ == '__main__'):
	app.run(debug=True)