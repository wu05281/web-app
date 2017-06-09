import os
from app import create_app, db
from app.models import User, Role, Post, Follow, Comment
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from flask_moment import Moment

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)
moment = Moment(app)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Post=Post, Follow=Follow)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
