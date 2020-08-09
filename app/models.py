from app import db

class Monster(db.Model):
    __tablename__ = "monster_info"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String,nullable=False,unique=True)

"""
Monster - (Foreign Key)
amount - integer
category - integer/string
"""
class MonsterCategories(db.Model):
    __table__name = "monster_category"
    id = db.Column(db.Integer,primary_key=True)
    category = db.Column(db.String,unique=True)

class MonsterLog(db.Model):
    __table__name = "monster_logs"
    id=db.Column(db.Integer,primary_key=True)
    amount = db.Column(db.Integer)
    # foreign key to monster
    monster_id = db.Column(db.Integer,db.ForeignKey('monster_id'),nullable=False)
    # forgien key to monstercategory 
    monster_category_id = db.Column(db.Integer,db.ForeignKey('monstercategories_id',nullable=False))
