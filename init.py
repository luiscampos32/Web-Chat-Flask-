import os.path
import flask
import sys
from flask_script import Manager
from flask_socketio import SocketIO

app = flask.Flask(__name__)
app.config.from_pyfile('settings.py')

app.content_root = os.path.dirname(app.root_path)
app.content_root = app.root_path

manager = Manager(app)
socketio = SocketIO(app)

recip_sockets = {}