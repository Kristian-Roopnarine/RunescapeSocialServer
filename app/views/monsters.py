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
    monster = Monster.query.get(id)
    return jsonify(monster.serialize)
    

@monster_blueprint.route('/',methods=['POST'])
def create_monster():
    if not request.json:
        abort(400)

    if 'name' not in request.json or request.json.get('name') == '':
        abort(400)

    monster = Monster(name=request.json.get('name'))
    db.session.add(monster)
    db.commit()
    return jsonify(monster)

@monster_blueprint.route('/<int:id>/',methods=['PUT','DELETE'])
def edit_monster(id):
    if not request.json:
        abort(400)

    monster = Monster.query.filter_by(id=id).get_or_404(description="That monster does not exist.")
    if request.method == 'DELETE':
        db.session.delete(monster)
    else:
        monster.name = request.json.get('name',monster.name)
        db.session.commit()
        return jsonify(monster)