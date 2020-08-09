from . import db



class Monster(db.Model):
    __tablename__ = "monster_info"

    name = db.column(db.String)


# monster log 
