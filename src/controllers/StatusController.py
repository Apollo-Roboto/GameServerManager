from controllers import app
import logging
logger = logging.getLogger(__name__)

@app.route("/ping", methods=["GET"])
def ping():
	logger.info("ping")
	return "🤖", 200