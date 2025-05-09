from flask import Flask, request, jsonify
from flask_cors import CORS
from routes.auth_routes import auth_bp
from routes.exercise_routes import exercise_bp
from routes.diet_routes import diet_bp
from db import get_connection

app = Flask(__name__)
CORS(app)

# 블루프린트 
app.register_blueprint(auth_bp)
app.register_blueprint(exercise_bp)
app.register_blueprint(diet_bp)

# 간단한 상태 확인용 라우터
@app.route('/test')
def test():
    return "Flask is running!"

# DB 테스트 라우터
@app.route('/db-test')
def db_test():
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users")  
            result = cursor.fetchall()
        conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=60020,
        debug=True  # ✅ 자동 새로고침 on
    )

