from flask import Flask
from flask_compress import Compress

app = Flask(__name__)
compress = Compress()
compress.init_app(app)

from controllers import GameStarterController
from controllers import StatusController