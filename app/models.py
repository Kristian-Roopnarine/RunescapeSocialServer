from app import db

class Monster(db.Model):
    __tablename__ = "monster_info"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String,nullable=False)
    level = db.Column(db.Integer,nullable=False),
    monster_id = db.Column(db.Integer,nullable=False,unique=True)

    @property
    def serialize(self):
        return {
            "id":self.id,
            "name":self.name,
            "combat_level":self.level,
            "monster_id":self.monster_id
        }

class MonsterCategories(db.Model):
    __tablename__ = "monster_category"
    id = db.Column(db.Integer,primary_key=True)
    category = db.Column(db.String,unique=True)

    @property
    def serialize(self):
        return {
            "id":self.id,
            "category":self.category
        }

class MonsterLog(db.Model):
    __tablename__ = "monster_logs"
    id=db.Column(db.Integer,primary_key=True)
    amount = db.Column(db.Integer)
    monster_id = db.Column(db.Integer,db.ForeignKey('monster_info.monster_id'),nullable=False)
    monster = db.relationship('Monster',backref=db.backref('monster_info',lazy=True))
    
    monster_category_id = db.Column(db.Integer,db.ForeignKey('monster_category.id'),nullable=False)
    monster_category = db.relationship('MonsterCategories',backref=db.backref('monster_categories',lazy=True))

    @property
    def serialize(self):
        return {
            "id":self.id,
            "amount":self.amount,
            "monster":self.monster.serialize
            "monster_category":self.monster_category.category
        }
