# manage.py

import unittest

from flask import redirect
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app, db


migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


@app.route('/')
def main():
    """Redirect to api endpoints"""

    return redirect('/apidocs')


if __name__ == '__main__':
    manager.run()
