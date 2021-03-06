from flask import (
    Blueprint,flash,g,redirect,request,session,url_for,jsonify,abort
)

from app.models import Monster,db

monster_blueprint = Blueprint("monster_blueprint",__name__,url_prefix="/monsters")

# CRUD for monster information

@monster_blueprint.route('/',methods=['GET'])
def all_monsters():
    monster_list = Monster.query.all()
    return jsonify([monster.serialize for monster in monster_list])

@monster_blueprint.route('/<int:id>/',methods=['GET'])
def get_monster(id):
    monster = Monster.query.filter_by(monster_id=id).first_or_404(description = "Could not find the monster.")
    return jsonify(monster.serialize)
    
@monster_blueprint.route('/',methods=['POST'])
def create_monster():

    if not request.json:
        abort(400)

    # handle verification on front end
    if 'name' not in request.json or request.json.get('name') == '':
        abort(400)

    monster = Monster(name=request.json.get('name'),level=request.json.get("combat_level"),monster_id=request.json.get('monster_id'))
    db.session.add(monster)
    db.session.commit()
    return jsonify(monster.serialize)

@monster_blueprint.route('/<int:id>/',methods=['PUT','DELETE'])
def edit_monster(id):
    
    monster = Monster.query.filter_by(monster_id=id).first_or_404(description="That monster does not exist.")
    if request.method == 'DELETE':
        db.session.delete(monster)
        db.session.commit()
        return jsonify({'monster':f'{monster.name} was successfully deleted.'})
    elif request.method == 'PUT':
        monster.name = request.json.get('name',monster.name)
        db.session.commit()
        return jsonify(monster.serialize)