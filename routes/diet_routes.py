from flask import Blueprint, request, jsonify
from services.diet_service import *

diet_bp = Blueprint('diet', __name__)

@diet_bp.route('/flask/diet/search', methods=['GET'])
def diet_search():
    name = request.args.get('name', '')
    results = search_diets(name)
    return jsonify(results)

@diet_bp.route('/flask/diet/recommend', methods=['GET'])
def diet_recommend():
    goal = request.args.get('goal', '다이어트')
    results = recommend_diets(goal)
    return jsonify(results)

@diet_bp.route('/flask/diet/info', methods=['PUT'])
def update_diet_info():
    data = request.get_json()
    name = data.get("name")
    new_type = data.get("type")
    new_goal = data.get("goal")

    result = update_diet(name, new_type, new_goal)
    return jsonify(result)

