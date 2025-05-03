# 임시 데이터베이스 (DB 열리면 실제 pymysql로 교체)
dummy_users = []

def signup_user(data):
    for user in dummy_users:
        if user['uid'] == data['uid']:
            return {"message": "이미 존재하는 아이디입니다."}
    
    dummy_users.append(data)
    return {"message": "회원가입 성공", "user": data}

def login_user(data):
    for user in dummy_users:
        if user['uid'] == data['uid'] and user['pass'] == data['pass']:
            return {"message": "로그인 성공", "user": user}
    return {"message": "로그인 실패"}

def delete_user_by_uid(uid, password):
    global dummy_users
    for user in dummy_users:
        if user["uid"] == uid and user["pass"] == password:
            dummy_users = [u for u in dummy_users if u["uid"] != uid]
            return {"message": "탈퇴 성공", "uid": uid}
    return {"message": "탈퇴 실패 - 정보 불일치"}

def update_user_profile(uid, name=None, goal=None):
    for user in dummy_users:
        if user["uid"] == uid:
            if name:
                user["name"] = name
            if goal:
                user["goal"] = goal
            return {"message": "프로필 수정 성공", "user": user}
    return {"message": "수정 실패 - 사용자 없음"}

def update_user_body(uid, height=None, weight=None, bmi=None):
    for user in dummy_users:
        if user["uid"] == uid:
            if height:
                user["height"] = height
            if weight:
                user["weight"] = weight
            if bmi:
                user["bmi"] = bmi
            return {"message": "신체정보 수정 성공", "user": user}
    return {"message": "수정 실패 - 사용자 없음"}





