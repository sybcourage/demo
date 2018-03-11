from flask_script import Manager, Server
from app.model import db, User
from app.temper_web import app

manager = Manager(app)
manager.add_command("server", Server())

@manager.shell
def make_shell_context():
    return dict(app=app, db=db, User=User)



