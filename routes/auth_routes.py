from flask import Blueprint, request, jsonify
from services.auth_service import *

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json
    return jsonify(signup_user(data))

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    return jsonify(login_user(data))

@auth_bp.route('/user', methods=['DELETE'])
def delete_user():
    data = request.get_json()
    uid = data.get("uid")
    password = data.get("pass")

    result = delete_user_by_uid(uid, password)
    return jsonify(result)

@auth_bp.route('/user/profile', methods=['PUT'])
def update_profile():
    data = request.get_json()
    uid = data.get("uid")
    name = data.get("name")
    goal = data.get("goal")

    result = update_user_profile(uid, name, goal)
    return jsonify(result)

@auth_bp.route('/user/body', methods=['PUT'])
def update_body_info():
    data = request.get_json()
    uid = data.get("uid")
    height = data.get("height")
    weight = data.get("weight")
    bmi = data.get("bmi")

    result = update_user_body(uid, height, weight, bmi)
    return jsonify(result)

@auth_bp.route('/logout', methods=['POST'])
def logout():
    response = jsonify({"message": "로그아웃 되었습니다."})
    # 쿠키에 저장된 토큰 제거 (옵션)
    response.set_cookie('access_token', '', expires=0)
    return response
