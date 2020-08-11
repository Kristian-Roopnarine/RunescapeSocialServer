from flask_testing import TestCase
from flask import jsonify
import sys
import unittest
import json
sys.path.append('./')
from app.models import MonsterCategories,db
from base import BaseTestCase
from sqlalchemy.exc import IntegrityError

TEST_DB = "test.db"

def create_category(category):
    db.session.add(MonsterCategories(category=category))
    db.session.commit()

def get_category(self,id):
    return self.client.get(
        f'/monster-category/{id}/'
    )

class TestMonsterCategoryEndpoint(BaseTestCase):

    def test_monster_category_create(self):
        create_category("Bossing")
        mon_category = MonsterCategories.query.get(1)
        self.assertEqual(mon_category.category,"Bossing")

    def test_monster_category_unique_constraint(self):
        create_category("Bossing")
        self.assertRaises(IntegrityError,create_category,"Bossing")
    
    def test_get_monster_category(self):
        create_category("Bossing")
        response = get_category(self,1)
        self.assertEqual(response.status_code,200)

        self.assertEqual(json.loads(response.data)['category'],"Bossing")