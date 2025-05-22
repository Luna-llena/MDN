import json
from flask import Blueprint, request, jsonify
from numpy import indices
import pandas as pd
from services.db_utils import save_recommendation_log
from services.exercise_recommendation import get_exercise_recommendation
from services.exercise_service import *
from db import get_connection

exercise_bp = Blueprint('exercise', __name__)

@exercise_bp.route('/flask/exercise/search', methods=['GET'])
def search():
    name = request.args.get('name', '')
    results = search_exercises(name)
    return jsonify(results)

@exercise_bp.route('/flask/exercise/recommend', methods=['GET'])
def recommend():
    goal = request.args.get('goal', 'default')
    results = recommend_exercises(goal)
    return jsonify(results)

@exercise_bp.route('/flask/exercise/info', methods=['PUT'])
def update_exercise_info():
    data = request.get_json()
    name = data.get("name")
    new_type = data.get("type")
    new_goal = data.get("goal")

    result = update_exercise(name, new_type, new_goal)
    return jsonify(result)

@exercise_bp.route('/flask/exercise/recommend', methods=['POST'])
def recommend_exercise():
    # 1) 클라이언트 JSON 파싱 및 uid 추출
    data = request.get_json() or {}
    uid = data.get('uid')  
    if not uid:
        return jsonify({
            "status": "error",
            "data": None,
            "error": "Missing required field: uid"
        }), 400

    # 2) 사용자 입력(user_input) 구성
    user_input = {
        'Sex':                 data.get('sex', 'Male'),
        'Age':                 data.get('age', 25),
        'Height':              data.get('height', 1.75),
        'Weight':              data.get('weight', 70),
        'Hypertension':        data.get('hypertension', 'No'),
        'Diabetes':            data.get('diabetes', 'No'),
        'BMI':                 data.get('bmi', round(data.get('weight',70) / (data.get('height',1.75)**2), 1)),
        'Level':               data.get('level', 'Normal'),
        'Fitness Goal':        data.get('goal', 'Weight Loss'),
        'Fitness Type':        data.get('fitness_type', 'Cardio'),
        'Workout Environment': data.get('location_preference', 'Home'),
        'Equipment':           data.get('equipment', 'none').lower(),
    }

    # 3) AI 추천 호출
    recs = get_exercise_recommendation(user_input)

    # 4) DB에 추천 기록 저장
    save_recommendation_log(uid, recs)

    # 5) 응답 반환
    return jsonify({
        "status": "success",
        "data": {
            "uid": uid,
            "recommended": recs
        },
        "error": None
    }), 200

@exercise_bp.route('/flask/exercise/log', methods=['POST'])
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

@exercise_bp.route('/flask/record', methods=['POST'])
def save_exercise_record():
    conn = None  

    try:
        data = request.json
        user_id = data['user_id']
        recommended_by = data.get('recommended_by', 'preset')
        exercises = data['recommended_exercises']

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO exercise_logs (user_id, recommended_by, recommended_exercises)
            VALUES (%s, %s, %s)
        """, (user_id, recommended_by, json.dumps(exercises)))
        conn.commit()

        log_id = cursor.lastrowid
        return jsonify({
            "status": "success",
            "message": "운동 추천 기록 저장 완료",
            "log_id": log_id
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

    finally:
        if conn is not None:
            conn.close()


        
@exercise_bp.route('/flask/complete', methods=['POST'])
def complete_exercise():
    data = request.json
    log_id = data['log_id']  # react에서 넘겨받은 log_id 사용

    # 요청이 들어오면 바로 5점 고정 부여
    completed_sets = 1  # 최소 1세트 수행했다고 가정
    score = 5

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE exercise_logs
            SET completed_sets = %s, score = %s
            WHERE id = %s
        """, (completed_sets, score, log_id))
        conn.commit()
        return jsonify({"status": "success", "message": "운동 수행 완료 기록 반영됨 (5점 부여)"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    finally:
        conn.close()

#주간 집계 랭킹 API
@exercise_bp.route('/flask/rank/weekly', methods=['GET'])
def get_weekly_rank():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT user_id, SUM(score) as total_score
            FROM exercise_logs
            WHERE timestamp >= NOW() - INTERVAL 7 DAY
            GROUP BY user_id
            ORDER BY total_score DESC
        """)
        result = cursor.fetchall()
        conn.close()

        return jsonify({"status": "success", "data": result})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
