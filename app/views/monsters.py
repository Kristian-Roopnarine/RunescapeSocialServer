from flask import (
    Blueprint,flash,g,redirect,request,session,url_for,jsonify,abort
)

from app.models import Monster,db

monster_blueprint = Blueprint("monster_blueprint",__name__,url_prefix="/monsters")

# CRUD for monster information


@monster_blueprint.route('/',methods=['GET'])
def all_monsters():
    monster_list = Monster.query.all()
    return jsonify(monster_list)

@monster_blueprint.route('/',methods=['POST'])
def create_monster():
    # get form data
    # create monster
    # save to db 
    # return monster info
    pass

