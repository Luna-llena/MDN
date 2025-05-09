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

@exercise_bp.route('/exercise/recommend', methods=['POST'])
def recommend_exercise():
    data = request.get_json()
    uid = data.get("uid")
    goal = data.get("goal")
    equipment = data.get("equipment")
    time = data.get("time")

    # 나중에 AI가 올리면 바꿀거임 건들 ㄴㄴ
    recommended = recommend_exercises(goal, equipment, time)
    return jsonify({"uid": uid, "recommended": recommended})

@exercise_bp.route('/exercise/log', methods=['POST'])
def log_exercise():
    print("운동 기록 API 요청 정상 도착")
    data = request.get_json()
    uid = data.get("uid")
    name = data.get("exercise_name")
    sets = data.get("sets")
    duration = data.get("duration")
    is_completed = data.get("is_completed")

    result = save_exercise_log(uid, name, sets, duration, is_completed)
    return jsonify(result)

