import logging
import sys
from logging.config import dictConfig

# Sets Logging Configurations
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '>> %(asctime)s [%(levelname)s] >> %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

from gevent import monkey
monkey.patch_all()
from gevent.pywsgi import WSGIServer

from core import AppConfig, Security
from controllers import app

logger = logging.getLogger(__name__)
config = AppConfig.getInstance()

if(__name__ == '__main__'):

	# Generate a token
	if(len(sys.argv) > 1):
		if(sys.argv[1] == "generatetoken"):
			Security.generateToken()
			logger.info("Token generated")
		else:
			logger.info("Unknown argument")
			
	else:
		if(config.flaskDebug):
			app.run(
				debug=True,
				host=config.flaskHost,
				port=config.flaskPort
			)
		else:
			logger.info("Starting flask server...")
			http_server = WSGIServer((config.flaskHost, config.flaskPort), app)
			logger.info(f"Listening on {config.flaskHost}:{config.flaskPort}")
			http_server.serve_forever()

