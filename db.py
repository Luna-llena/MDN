import pymysql

def get_connection():
    return pymysql.connect(
        host="localhost",
        user="dbid251",
        password="dbpass251",
        database="db25120",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )

