from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def hello():
	return {"msg":"Hello World!"}, 200

if(__name__ == '__main__'):
	app.run(debug=True)