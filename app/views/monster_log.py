from flask import (
    Blueprint,url_for,redirect,g,flash,request,jsonify,abort
)

from app.models import Monster,MonsterCategories,db,MonsterLog


monster_log_blueprint = Blueprint("monster_log_blueprint",__name__,url_prefix='/monster-log')


@monster_log_blueprint.route('/',methods=['GET'])
def get_all_monster_logs():
    monster_logs = MonsterLog.query.all()
    return jsonify([monster_log.serialize for monster_log in monster_logs])

@monster_log_blueprint.route('/',methods=['POST'])
def create_monster_log():
    
    if not request.json:
        abort(400)
    
    """
    if 'monster_id' not in request.json or 'category_id' not in request.json or 'amount' not in request.json:
        abort(400)
    """
    monster = Monster.query.filter_by(monster_id=request.json.get('monster_id')).first_or_404(description='Could not find that monster.')

    monster_category = MonsterCategories.query.get_or_404(request.json.get('category_id'),description="Could not find that category.")

    monster_log = MonsterLog(
        amount=request.json.get('amount'),
        monster=monster,
        monster_category=monster_category
    )

    db.session.add(monster_log)
    db.session.commit()
    return jsonify(monster_log.serialize)

@monster_log_blueprint.route('/<int:id>/',methods=['GET'])
def get_monster_log(id):
    monster_log = MonsterLog.query.get_or_404(id,description="Could not find that monster log.")
    return jsonify(monster_log.serialize)

@monster_log_blueprint.route('/<int:id>/',methods=['PUT','DELETE'])
def update_monster_log(id):
    monster_log = MonsterLog.query.get(id)

    if request.method == 'PUT':
        if monster_log.monster_id != request.json.get('monster_id'):
            monster = Monster.query.filter_by(monster_id=request.json.get('monster_id')).first_or_404()
            monster_log.monster = monster
        if monster_log.monster_category_id != request.json.get('category_id'):
            monster_category = MonsterCategories.query.get_or_404(request.json.get('category_id'))
            monster_log.monster_category=monster_category
        
        monster_log.amount = request.json.get('amount')
        db.session.add(monster_log)
        db.session.commit()
        return jsonify(monster_log.serialize)
        
    elif request.method == 'DELETE':
        db.session.delete(monster_log)
        db.session.commit()
        return jsonify({'success':'The monster log was deleted.'})

    return jsonif({"Wrong request."})