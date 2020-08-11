from flask_testing import TestCase
from flask import jsonify
import sys
import unittest
import json
sys.path.append('./')
from app.models import Monster,db
from base import BaseTestCase
from sqlalchemy.exc import IntegrityError


TEST_DB = "test.db"

def create_monster(entered_name):
    db.session.add(Monster(name=entered_name))
    db.session.commit()

def get_all_monsters(self):
    return self.client.get('/monsters/')

def get_monster_with_id(self,monster_id):
    return self.client.get(f"/monsters/{monster_id}/")

def create_monster_endpoint(self,name):
    return self.client.post(
        '/monsters/',
        data = json.dumps(dict(
            name=name
        )),
        content_type="application/json"
    )

def update_monster_endpoint(self,id):
    return self.client.put(
        f'/monsters/{id}/',
        data = json.dumps(dict(
            name="Vorkath"
        )),
        content_type="application/json"
    )

def delete_monster_endpoint(self,id):
    return self.client.delete(f'/monsters/{id}/')

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

"""
TODO: move to monster log tests
    def test_create_monster_log(self):
        create_monster("Zulrah")
        create_monster_category("Bossing")
        zulrah = Monster.query.get(1)
        monster_category = MonsterCategories.query.get(1)
        monster_record = MonsterLog(amount=5,monster=zulrah,monster_category=monster_category)
        db.session.add(monster_record)
        db.session.commit()
        monster_record = MonsterLog.query.get(1)
        self.assertEqual(monster_record.amount,5)
        self.assertEqual(monster_record.monster.name,"Zulrah")
        self.assertEqual(monster_record.monster_category.category,"Bossing")
"""

class TestMonsterBlueprint(BaseTestCase):

    def test_get_all_monsters(self):
        create_monster("Zulrah")
        create_monster("Vorkath")
        create_monster("Barrows")
        create_monster("Olm")
        response = get_all_monsters(self)
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(json.loads(response.data)),4)
    
    def test_get_monster_with_id(self):
        create_monster("Zulrah")
        response = get_monster_with_id(self,1)
        monster = json.loads(response.data)
        self.assertEqual(response.status_code,200)
        self.assertEqual(monster['name'],"Zulrah")

    def test_get_monster_when_id_does_not_exist(self):
        create_monster("Zulrah")
        response = get_monster_with_id(self,2)
        self.assertEqual(response.status_code,404)

    def test_create_monster_endpoint(self):
        response = create_monster_endpoint(self,"Zulrah")
        self.assertEqual(response.status_code,200)
        monster = json.loads(response.data)
        self.assertEqual(monster['name'],"Zulrah")
    
    def test_create_monster_no_name(self):
        response = create_monster_endpoint(self,"")
        self.assertEqual(response.status_code,400)
    
    def test_update_monster_name(self):
        create_monster("Zulrah")
        response = update_monster_endpoint(self,1)
        self.assertEqual(response.status_code,200)
        updated_monster = Monster.query.get(1)
        self.assertEqual(updated_monster.name,"Vorkath")

    def test_delete_monster(self):
        create_monster("Zulrah")
        create_monster("Vorkath")
        response = delete_monster_endpoint(self,1)
        self.assertEqual(response.status_code,200)
        response = delete_monster_endpoint(self,2)
        self.assertEqual(response.status_code,200)



if __name__ == "__main__":
    unittest.main()