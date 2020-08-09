from flask_testing import TestCase
import sys
import unittest

sys.path.append('./')
from app.models import Monster,db
from base import BaseTestCase


TEST_DB = "test.db"

class TestMonsterModel(BaseTestCase):

    def test_create_monster_data(self):
        mnstr = Monster(name="test")

        db.session.add(mnstr)
        db.session.commit()

        monster = Monster.query.get(1)
        total_monsters = Monster.query.all()
        self.assertEqual(monster.name,"test")
        self.assertEqual(len(total_monsters),1)

if __name__ == "__main__":
    unittest.main()