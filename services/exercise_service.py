from db import get_connection

# 임시 운동 데이터
dummy_exercises = [
    {"name": "푸쉬업", "type": "상체", "goal": "근력"},
    {"name": "스쿼트", "type": "하체", "goal": "근력"},
    {"name": "버피", "type": "전신", "goal": "다이어트"},
    {"name": "플랭크", "type": "코어", "goal": "체형교정"},
]

def search_exercises(name):
    return [ex for ex in dummy_exercises if name in ex["name"]]

def recommend_exercises(goal):
    return [ex for ex in dummy_exercises if ex["goal"] == goal] or dummy_exercises

def search_exercises(name):
    return [ex for ex in dummy_exercises if name in ex["name"]]

def recommend_exercises(goal):
    return [ex for ex in dummy_exercises if ex["goal"] == goal] or dummy_exercises

def update_exercise(name, new_type=None, new_goal=None):
    for ex in dummy_exercises:
        if ex["name"] == name:
            if new_type:
                ex["type"] = new_type
            if new_goal:
                ex["goal"] = new_goal
            return {"message": "운동 정보 수정 성공", "exercise": ex}
    return {"message": "수정 실패 - 운동 없음"}

# 나중에 AI가 다 완성되면 바꿀거임 건들 ㄴㄴ
def recommend_exercises(goal, equipment, time):
    dummy_recommend = [
        {"name": "스쿼트", "duration": "30초 x 3세트"},
        {"name": "버피", "duration": "20초 x 4세트"},
        {"name": "플랭크", "duration": "1분 x 2세트"}
    ]
    return dummy_recommend


def save_exercise_log(uid, name, sets, duration, is_completed):
    conn = get_connection()
    print("DB 연결 성공")
    try:
        with conn.cursor() as cursor:
            sql = """
                INSERT INTO exercise_logs (uid, exercise_name, sets, duration, is_completed)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (uid, name, sets, duration, is_completed))
        conn.commit()  
        return {"message": "운동 기록 저장 완료"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close() 
