from flask_testing import TestCase
from flask import jsonify
import sys
import unittest
import json
sys.path.append('./')
from app.models import MonsterCategories,db,Monster,MonsterLog
from base import BaseTestCase
from sqlalchemy.exc import IntegrityError

from tests.test_monster import create_monster
from tests.test_monster_category import create_category

TEST_DB = "test.db"


def create_monster_log(monster_name,combat_level,monster_id):
    create_monster(monster_name,combat_level,monster_id)
    monster = Monster.query.filter_by(monster_id=monster_id).first()
    monster_category = MonsterCategories.query.get(1)
    monster_log = MonsterLog(
        amount=1,
        monster=monster,
        monster_category=monster_category
    )

    db.session.add(monster_log)
    db.session.commit()

def get_all_monster_logs(self):
    return self.client.get('/monster-log/')

def get_monster_log(self,id):
    return self.client.get(f'/monster-log/{id}/')

def update_monster_log(self,id,monster_id,category_id,amount):
    return self.client.put(
        f'/monster-log/{id}/',
        data=json.dumps(dict(
            monster_id=monster_id,
            category_id=category_id,
            amount=amount
        )),
        content_type="application/json"
    )

def create_monster_log_endpoint(self,monster_id,category_id):
    return self.client.post(
        '/monster-log/',
        data=json.dumps(dict(
            amount=5,
            monster_id=monster_id,
            category_id=category_id
        )),
        content_type="application/json"
    )

def delete_monster_log_endpoint(self,id):
    return self.client.delete(
        f'/monster-log/{id}/'
    )

class TestMonsterLogModel(BaseTestCase):

    def test_monster_log_create(self):
        create_category("Bossing")
        create_monster_log("Zulrah",700,705)
        monster_log = MonsterLog.query.get(1)
        self.assertEqual(monster_log.monster.name,"Zulrah")
        self.assertEqual(monster_log.monster_category.category,"Bossing")
        self.assertEqual(monster_log.monster_id,705)

    def test_monster_log_serialize(self):
        create_category("Bossing")
        create_monster_log("Zulrah",700,705)
        monster_log = MonsterLog.query.get(1)
        serialized = monster_log.serialize
        self.assertEqual(serialized['amount'],1)
        self.assertEqual(serialized['monster'],{"id":1,"name":"Zulrah","combat_level":700,"monster_id":705})
        self.assertEqual(serialized['monster_category'],"Bossing")


class TestMonsterLogBlueprint(BaseTestCase):

    def test_get_all_monsters_endpoint(self):
        create_category("Bossing")
        create_monster_log("Zulrah",700,705)
        create_monster_log("Vorkath",700,706)

        response = get_all_monster_logs(self)
        self.assertEqual(response.status_code,200)
        monster_log = json.loads(response.data)
        self.assertEqual(len(monster_log),2)

    def test_get_monster_log_by_monster_log_id(self):
        create_category("Bossing")
        create_monster_log("Zulrah",700,705)
        response = get_monster_log(self,1)
        self.assertEqual(response.status_code,200)
        monster_log=json.loads(response.data)
        self.assertEqual(monster_log['monster']['monster_id'],705)

    def test_create_monster_log_endpoint(self):
        create_monster("Zulrah",700,705)
        create_category("Bossing")
        response = create_monster_log_endpoint(self,705,1)
        self.assertEqual(response.status_code,200)
        monster_log = json.loads(response.data)
        self.assertEqual(monster_log['amount'],5)

    def test_update_monster_log(self):
        create_category("Bossing")
        create_monster_log("Zulrah",700,705)
        create_monster_log("Vorkath",700,706)
        response = update_monster_log(self,1,706,1,4)
        self.assertEqual(response.status_code,200)
        monster_log = json.loads(response.data)
        self.assertEqual(monster_log['monster']['name'],'Vorkath')
        self.assertEqual(monster_log['amount'],4)

    def test_update_monster_doesnt_exist(self):
        create_category("Bossing")
        create_monster_log("Zulrah",700,705)
        create_monster_log("Vorkath",700,706)
        response = update_monster_log(self,1,708,1,4)
        self.assertEqual(response.status_code,404)
    
    def test_update_category_monster_log(self):
        create_category("Bossing")
        create_category("Slayer")
        create_monster_log("Zulrah",700,705)
        response = update_monster_log(self,1,705,2,4)
        self.assertEqual(response.status_code,200)
        monster_log = json.loads(response.data)
        self.assertEqual(monster_log['monster_category'],'Slayer')
        self.assertEqual(monster_log['monster']['name'],"Zulrah")

    def test_delete_monster_log(self):
        create_category("Bossing")
        create_monster_log("Zulrah",700,705)
        response = delete_monster_log_endpoint(self,1)
        self.assertEqual(response.status_code,200)
        self.assertEqual(json.loads(response.data),{'success':'The monster log was deleted.'})

        response2 = get_monster_log(self,1)
        self.assertEqual(response2.status_code,404)