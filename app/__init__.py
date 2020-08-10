import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    from .views.monsters import monster_blueprint

    app = Flask(__name__,instance_relative_config=False)
    app.config.from_object('config.Config')
    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(monster_blueprint)

    return app