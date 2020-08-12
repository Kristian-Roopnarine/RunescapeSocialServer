import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    from .views.monster import monster_blueprint
    from .views.monster_category import monster_category_blueprint
    from .views.monster_log import monster_log_blueprint

    app = Flask(__name__,instance_relative_config=False)
    app.config.from_object('config.Config')
    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(monster_blueprint)
    app.register_blueprint(monster_category_blueprint)
    app.register_blueprint(monster_log_blueprint)

    return app