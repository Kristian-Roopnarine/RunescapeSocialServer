from app import db

class Monster(db.Model):
    __tablename__ = "monster_info"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String,nullable=False,unique=True)

class MonsterCategories(db.Model):
    __tablename__ = "monster_category"
    id = db.Column(db.Integer,primary_key=True)
    category = db.Column(db.String,unique=True)

class MonsterLog(db.Model):
    __tablename__ = "monster_logs"
    id=db.Column(db.Integer,primary_key=True)
    amount = db.Column(db.Integer)
    monster_id = db.Column(db.Integer,db.ForeignKey('monster_info.id'),nullable=False)
    monster = db.relationship('Monster',backref=db.backref('monster_logs',lazy=True))
    
    monster_category_id = db.Column(db.Integer,db.ForeignKey('monster_category.id'),nullable=False)
    monster_category = db.relationship('MonsterCategories',backref=db.backref('monster_categories',lazy=True))
