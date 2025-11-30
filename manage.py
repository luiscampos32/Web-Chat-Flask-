import os, sys, re
import sys
from flask_script import Manager

import main as app_module
app = app_module.app


if hasattr(app_module, 'manager'):
    manager = app_module.manager
else:
    manager = Manager(app)


@manager.command
def initdb():
    if hasattr(app_module, 'db'):
        db = app_module.db
    elif 'init' in sys.modules and hasattr(sys.modules['init'], 'db'):
        db = sys.modules['init'].db
    else:
        raise RuntimeError('cannot find database object')

    print('initializing database')
    db.create_all(app=app)

@manager.command
def socketserver(debug=False, reload=False):
    if hasattr(app_module, 'socketio'):
        sio = app_module.socketio
        sio.run(app, debug=debug, use_reloader=reload)
    else:
        print('app does not define socketio, cannot run', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    manager.run()