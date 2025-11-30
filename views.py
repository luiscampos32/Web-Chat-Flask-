import io
import json
import flask
import base64
import os
import uuid

from init import app, socketio
from flask_socketio import send, emit, join_room

@app.route('/')
def index():
    return flask.render_template('index.html')
