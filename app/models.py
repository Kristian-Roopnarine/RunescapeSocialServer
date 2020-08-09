from app import db
class Monster(db.Model):
    __tablename__ = "monster_info"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String,nullable=False)


# monster log 
