from osrsbox import monsters_api
from .models import Monster,db

class PersistToDB:
    def add_to_db(self,item):
        db.session.add(item)
        db.session.commit()

class OSRSMonsters(PersistToDB):
    def __init__(self):
        self.monsters = monsters_api.load()

    def loop_through(self):
        for monster in self.monsters:
            monster = self.create_monster(monster.name,monster.combat_level,monster.id)
            self.add_to_db(monster)

    def create_monster(self,monster_name,combat_level,monster_id):
        return Monster(name=monster_name,level=combat_level,monster_id=monster_id)
