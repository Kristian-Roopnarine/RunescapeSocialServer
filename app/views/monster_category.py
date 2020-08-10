from flask import (
    Blueprint,g,flash,jsonify,abort,session
)

from app.models import db,MonsterCategories

monster_category_blueprint = Blueprint('monster_category_blueprint',__name__,url_prefix='/monster-category')

@monster_category_blueprint.route('/',methods=['GET'])
def get_categories():
    categories = MonsterCategories.query.all()
    return jsonify([category.serialize for category in categories])

@monster_category_blueprint.route('/',methods=['POST'])
def create_category():
    if not request.json:
        abort(400)
    
    if 'category' not in request.json or request.json.get('category') == '':
        abort(400)
    
    category = MonsterCategories(category=request.json.get('category'))
    db.session.add(category)
    db.session.commit()
    return jsonify(category.serialize)

@monster_category_blueprint.route('/<int:id>/',methods=['GET'])
def get_category(id):
    category = MonsterCategories.query.get_or_404(id)
    return jsonify(category.serialize)

@monster_category_blueprint.route('/<int:id>/',methods=['PUT','DELETE'])
def edit_or_delete(id):
    category = MonsterCategories.query.get_or_404(id)
    if request.method == 'DELETE':
        db.session.delete(category)
        return jsonify({'category':f'{category.category} was successfully deleted.'})
    elif request.method == 'PUT':
        category.category = request.json.get('category',category.category)
        db.session.commit()
        return jsonify(category.serialize)

