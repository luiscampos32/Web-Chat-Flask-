import flask
import flask_socketio
import views

from init import app, socketio
from flask_socketio import join_room, send, emit, leave_room

# Handles a client connecting to the server
@socketio.on('connect')
def on_connect():
    app.logger.info("Client connected: %s", flask.request.sid)

# Handles a client leaving a chat room
@socketio.on('disconnect')
def on_disconnect():
    room = flask.session['room']['key']
    leave_room(room)
    app.logger.info("Client disconnected: %s", flask.request.sid)

# Handles a client entering a chat room
@socketio.on('enterchat')
def on_enterchat(data):
    app.logger.info("entered server chat")
    username = data['name']
    room = data['room']
    flask.session['user'] = username
    join_room(room)
    views.rooms[room]['users'].append(data['name'])
    emit('joined', {
        'msg': data['name'] + 'has joined the chat.',
        'user': username,
        'sid': data['sid'],
        'users': views.rooms[room]['users']
    })

# Handles a chat message sent by a client
# Sends this information client side to update the chat window
@socketio.on('chat')
def on_chat(data):
    room = data['room']
    msg = data['message']
    user = data['user']
    emit('new-chat', {
        'msg': msg,
        'user': user
    }, room=room)

# Handles updating the user list when a user leaves the chat room
@socketio.on('updateList')
def update_list(data):
    views.rooms[data.room]['users'].remove(data.name)
    emit('updateList', {
        'users': views.rooms[data.room]['users']
    }, room=data.room)