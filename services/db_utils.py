# services/db_utils.py
import json
from db import get_db

def save_recommendation_log(uid: str, recs: list[str]):
    """
    exercise_logs 테이블에 uid와 추천 리스트를 남깁니다.
    나머 필드는 DEFAULT(0, CURRENT_TIMESTAMP 등)로 자동 채워져요.
    """
    db = get_db()
    sql = """
      INSERT INTO exercise_logs (
        uid,
        recommended_exercises
      ) VALUES (%s, %s)
    """
    rec_json = json.dumps(recs, ensure_ascii=False)
    with db.cursor() as cur:
        cur.execute(sql, (uid, rec_json))
    db.commit()
