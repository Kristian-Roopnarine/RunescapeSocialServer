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

def create_monster(entered_name,combat_level,monster_id):
    db.session.add(Monster(name=entered_name,level=combat_level,monster_id=monster_id))
    db.session.commit()

def get_all_monsters(self):
    return self.client.get('/monsters/')

def get_monster_with_id(self,monster_id):
    return self.client.get(f"/monsters/{monster_id}/")

def create_monster_endpoint(self,name,combat_level,monster_id):
    return self.client.post(
        '/monsters/',
        data = json.dumps(dict(
            name=name,
            combat_level=combat_level,
            monster_id = monster_id
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
        create_monster("test",700,705)
        monster = Monster.query.get(1)
        total_monsters = Monster.query.all()
        self.assertEqual(monster.name,"test")
        self.assertEqual(monster.monster_id,705)
        self.assertEqual(len(total_monsters),1)

    def test_monster_data_unique_constraint(self):
        create_monster("test",700,705)
        self.assertRaises(IntegrityError,create_monster,"test",700,705)


class TestMonsterBlueprint(BaseTestCase):

    def test_get_all_monsters(self):
        create_monster("Zulrah",700,705)
        create_monster("Vorkath",701,706)
        create_monster("Barrows",708,709)
        create_monster("Olm",1500,900)
        response = get_all_monsters(self)
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(json.loads(response.data)),4)
    
    def test_get_monster_with_id(self):
        create_monster("Zulrah",700,705)
        response = get_monster_with_id(self,705)
        monster = json.loads(response.data)
        self.assertEqual(response.status_code,200)
        self.assertEqual(monster['name'],"Zulrah")

    def test_get_monster_when_id_does_not_exist(self):
        create_monster("Zulrah",700,705)
        response = get_monster_with_id(self,2)
        self.assertEqual(response.status_code,404)

    def test_create_monster_endpoint(self):
        response = create_monster_endpoint(self,"Zulrah",700,705)
        self.assertEqual(response.status_code,200)
        monster = json.loads(response.data)
        self.assertEqual(monster['name'],"Zulrah")
    
    def test_create_monster_no_name(self):
        response = create_monster_endpoint(self,"",700,705)
        self.assertEqual(response.status_code,400)
    
    def test_update_monster_name(self):
        create_monster("Zulrah",700,705)
        response = update_monster_endpoint(self,705)
        self.assertEqual(response.status_code,200)
        updated_monster = Monster.query.filter_by(monster_id=705).first_or_404()
        self.assertEqual(updated_monster.name,"Vorkath")

    def test_delete_monster(self):
        create_monster("Zulrah",700,705)
        create_monster("Vorkath",705,701)
        response = delete_monster_endpoint(self,705)
        self.assertEqual(response.status_code,200)
        response = delete_monster_endpoint(self,701)
        self.assertEqual(response.status_code,200)
        response = get_monster_with_id(self,701)
        self.assertEqual(response.status_code,404)



if __name__ == "__main__":
    unittest.main()