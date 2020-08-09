import os
import unittest
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from flask import url_for

from app.models import db
import app

app = app.create_app()
migrate = Migrate(app,db)
manager = Manager(app)
manager.add_command('db',MigrateCommand)

@manager.command
def test():
    """ Runs the unit test without test coverage"""
    tests = unittest.TestLoader().discover('./tests/',pattern="test*.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == "__main__":
    manager.run()
    
