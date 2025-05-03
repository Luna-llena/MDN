# 임시 식단 데이터
dummy_diets = [
    {"name": "닭가슴살 샐러드", "type": "저칼로리", "goal": "다이어트"},
    {"name": "스테이크 정식", "type": "고단백", "goal": "벌크업"},
    {"name": "현미밥과 나물", "type": "균형잡힌", "goal": "체형유지"},
    {"name": "닭가슴살+고구마", "type": "고단백", "goal": "다이어트"},
]

def search_diets(name):
    return [d for d in dummy_diets if name in d["name"]]

def recommend_diets(goal):
    return [d for d in dummy_diets if d["goal"] == goal] or dummy_diets

def update_diet(name, new_type=None, new_goal=None):
    for d in dummy_diets:
        if d["name"] == name:
            if new_type:
                d["type"] = new_type
            if new_goal:
                d["goal"] = new_goal
            return {"message": "식단 정보 수정 성공", "diet": d}
    return {"message": "수정 실패 - 식단 없음"}
