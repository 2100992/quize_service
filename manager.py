from app import app, db

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell

from app.models import User

migrate = Migrate(app, db)

manager = Manager(app)

manager.add_command('db', MigrateCommand)

manager.add_command('shell', Shell)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}


if __name__ == "__main__":
    manager.run()
