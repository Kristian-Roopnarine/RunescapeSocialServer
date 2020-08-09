from flask_testing import TestCase
import sys
import unittest

sys.path.append('./')
from app.models import Monster,db
from base import BaseTestCase
from sqlalchemy.exc import IntegrityError


TEST_DB = "test.db"

def create_monster(entered_name):
    db.session.add(Monster(name=entered_name))
    db.session.commit()

class TestMonsterModel(BaseTestCase):

    def test_create_monster_data(self):
        create_monster("test")
        monster = Monster.query.get(1)
        total_monsters = Monster.query.all()
        self.assertEqual(monster.name,"test")
        self.assertEqual(len(total_monsters),1)

    def test_monster_data_unique_constraint(self):
        create_monster("test")
        self.assertRaises(IntegrityError,create_monster,"test")

if __name__ == "__main__":
    unittest.main()