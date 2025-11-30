import io
import json
import flask
import base64
import os
import uuid

from init import app, socketio
from flask_socketio import send, emit, join_room

rooms = {}

# Sets up a CSRF token before each request if not already present
@app.before_request
def setup_csrf():
    if 'csrf_token' not in flask.session:
        flask.session['csrf_token'] = base64.b64encode(os.urandom(32)).decode('ascii')

# Sets up the user in the global context before each request if logged in
@app.before_request
def setup_user():
    if 'user' in flask.session:
        flask.g.user = flask.session['user']

# Defines a simple route for the index page
@app.route('/')
def index():
    return flask.render_template('index.html')

"""
Defines a route to handle chat room creation.
Generates a unique key for each new chat room and
stores it in the rooms dictionary with an empty list of users.
Redirects the user to the newly created chat room.
"""
@app.route('/new-chat', methods=['POST'])
def new_chat():
    topic = flask.request.form['topic']
    key = base64.urlsafe_b64encode(uuid.uuid4().bytes)[:12]
    key = key.decode('utf-8')
    rooms.update({key: {'topic': topic, 'users': [], 'key': key}})
    return flask.redirect(flask.url_for('handle_room', key=key), code=303)

# Defines a route to handle individual chat rooms based on a unique key
@app.route('/<key>')
def handle_room(key):
    if key not in rooms:
        flask.abort(404)
    room = rooms[key]
    # Renders the chatroom template with the room details and CSRF token
    return flask.render_template('chatroom.html', room=room, csrf_token=flask.session['csrf_token'])