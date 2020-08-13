from .models import Monster,db

class PersistToDB:

    def add_to_db(self,item):
        db.session.add(item)
        db.session.commit()


class OSRSMonsters(PersistToDB):

    def create_monster(self,monster_name,combat_level,monster_id):
        return Monster(name=monster_name,level=combat_level,monster_id=monster_id)

