from flask import Blueprint, request, jsonify
from services.exercise_service import *

exercise_bp = Blueprint('exercise', __name__)

@exercise_bp.route('/exercise/search', methods=['GET'])
def search():
    name = request.args.get('name', '')
    results = search_exercises(name)
    return jsonify(results)

@exercise_bp.route('/exercise/recommend', methods=['GET'])
def recommend():
    goal = request.args.get('goal', 'default')
    results = recommend_exercises(goal)
    return jsonify(results)

@exercise_bp.route('/exercise/info', methods=['PUT'])
def update_exercise_info():
    data = request.get_json()
    name = data.get("name")
    new_type = data.get("type")
    new_goal = data.get("goal")

    result = update_exercise(name, new_type, new_goal)
    return jsonify(result)


