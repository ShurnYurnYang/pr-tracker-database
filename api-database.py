import psycopg2
from flask import Flask, request, jsonify
from datetime import datetime

connect_info = {
    "host": "containers-us-west-114.railway.app",
    "database": "railway",
    "user": "postgres",
    "password": "H6pKTOqR8rdL8YynetAv"
}

def query_execute(query, param = None):
    conn = psycopg2.connect(**connect_info)
    cur = conn.cursor()

    if param:
        cur.execute(query, param)
    else:
        cur.execute(query)

    result = cur.fetchall()

    conn.commit()

    cur.close()
    conn.close()

    return result

app = Flask(__name__)

## API FUNCTIONS:
## 1. Enter new user -> enters new user into 'users' table -> gives hashed password and discord-id if applicable
## 2. Enter new PR -> enters new pr data into 'historical' table -> generate appropriate graphs using mathplotlib
## 3. Get user info -> gets user information -> gets hashed password and discord-id
## 4. Get latest PR entry -> gets latest PR entry for specific user -> includes graphs

## 1. get user info
@app.route('/get_user', methods=['GET'])
def get_user():
    username = request.args.get('user_id')

    if username:
        query = "SELECT * FROM users WHERE username = (%s);"
        param = (username)
        
        try:
            user_data = query_execute(query, param)
        except Exception as error:
            return jsonify({"message": f"Server error, please try again later. Error code: {error}"}), 500
        
        if user_data:
            return jsonify(user_data), 200
        else:
            return jsonify({"message": "User not found"}), 404
    else:
        return jsonify({"message': 'Missing username parameter"}), 400
    
## 2. enter new PR info
@app.route('/insert_pr', methods=['POST'])
def insert_new_pr():
    data = request.get_json()

    if data:
        query = "INSERT INTO historical (user_id, record_date, pr) VALUES (%s, %s, ROW(%s, %s, %s, %s));"
        param = (data['user_id'], datetime.strptime(data['record_date'], "%Y-%m-%d").date(), data['pr']['name'], data['pr']['bench'], data['pr']['squat'], data['pr']['deadlift'])
        
        try:
            query_execute(query, param)
        except Exception as error:
            return jsonify({"message": f"Server error, please try again later. Error code: {error}"}), 500
        
        return jsonify({"message": "Data insertion success"}), 201
    else:
        return jsonify({"message": "Data not found"}), 404