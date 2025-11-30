from init import app, socketio

import views
import api

if __name__ == '__main__':
    socketio.run(app)