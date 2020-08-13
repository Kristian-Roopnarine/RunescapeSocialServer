import os
import unittest
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from flask import url_for
from osrsbox import monsters_api

from app.models import db
from app.utils import OSRSMonsters
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

@manager.command
def create_monsters_db():
    monsters = monsters_api.load()
    saved_to_db = {}
    osrs_monsters = OSRSMonsters()
    for monster in monsters:
        if monster.name in saved_to_db and saved_to_db[monster.name]['combat_level'] == monster.combat_level:
            continue
        mon = osrs_monsters.create_monster(monster.name,monster.combat_level,monster.id)
        osrs_monsters.add_to_db(mon)

        saved_to_db[monster.name] = {"combat_level":monster.combat_level}


if __name__ == "__main__":
    manager.run()
    
