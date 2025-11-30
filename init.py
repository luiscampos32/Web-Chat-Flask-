import os.path
import flask
import sys
from flask_script import Manager
from flask_socketio import SocketIO

app = flask.Flask(__name__)
app.config.from_pyfile('settings.py')

manager = Manager(app)
socketio = SocketIO(app)

