import psycopg2
import bcrypt

from flask import Flask, request, jsonify
from datetime import datetime

connect_info = { # Python dictionary for the database connection info
    "host": "containers-us-west-114.railway.app",
    "database": "railway",
    "user": "postgres",
    "password": "H6pKTOqR8rdL8YynetAv"
}

def query_execute(query, param = None): # function to execute sql query given query and param
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

def bcrypt_check(reference_hashed, test_raw): # function that checks an unhashed value against a hashed value | returns boolean
    return bcrypt.checkpw(test_raw.encode('utf-8'), reference_hashed)

app = Flask(__name__)

# API FUNCTIONS:
# 1. Enter new user -> enters new user into 'users' table -> gives hashed password and discord-id if applicable
# 2. Enter new PR -> enters new pr data into 'historical' table -> generate appropriate graphs using mathplotlib
# 3. Get user info -> gets user information -> gets hashed password and discord-id
# 4. Get latest PR entry -> gets latest PR entry for specific user -> includes graphs
# Keep these API functions simple for now, add additional features when web-app development starts

# 1. enter new user
@app.route('/user', methods=['POST'])
def insert_new_user():
    data = request.get_json()
    query = "INSERT INTO users (username, discord_id_hash) VALUES (%s, %s);"

    if data:
        ##hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        hashed_discord_id = bcrypt.hashpw(data['discord_id'].encode('utf-8'), bcrypt.gensalt())
        param = (data['username'], hashed_discord_id)

        try:
            query_execute(query, param)
        except Exception as error:
            return jsonify({"message": f"Server error, please try again later. Error code: {error}"}), 500

        return jsonify({"message": "User registered successfully"}), 201
    else:
        return jsonify({"message": "Data not found"}), 404
    
# 2. enter new PR info
@app.route('/pr', methods=['POST'])
def insert_new_pr():
    data = request.get_json()

    if data:
        query = "INSERT INTO historical (user_id, record_date, pr) VALUES (%s, %s, ROW(%s, %s, %s, %s));"
        param = (data['user_id'], datetime.strptime(data['record_date'], "%Y-%m-%d").date(), data['pr']['name'], data['pr']['bench'], data['pr']['squat'], data['pr']['deadlift'])
        
        try:
            query_execute(query, param)
            query_execute("SELECT * FROM historical ORDER BY record_date") #Orders the database after every entry
        except Exception as error:
            return jsonify({"message": f"Server error, please try again later. Error code: {error}"}), 500
        
        return jsonify({"message": "Data insertion success"}), 201
    else:
        return jsonify({"message": "Data not found"}), 404
    
# 3. Check discord_id endpoint
@app.route('/check_discord_id', methods=['POST'])
def verify_discord_id():
    data = request.get_json()

    if data:
        query = "SELECT discord_id_hash FROM users WHERE username = (%s);"
        param = (data['username'])
        
        try:
            discord_id_hash = query_execute(query, param)
        except Exception as error:
            return jsonify({"message": f"Server error, please try again later. Error code: {error}"}), 500
        
        if discord_id_hash:
            if bcrypt_check(discord_id_hash, data['discord_id']):
                return jsonify({"message": "User verified", "verified": True}), 200
            else:
                return jsonify({"message": "Incorrect user", "verified": False}), 401
        else:
            return jsonify({"message": "User not found"}), 404
    else:
        return jsonify({"message': 'Missing username parameter"}), 400
    
# 4. Get latest entry given username
@app.route('/latest_pr_username', methods=['GET'])
def get_latest_entry_discord_id():
    username = request.args.get('username')

    if username:
        try:
            query = "SELECT user_id FROM users WHERE username = (%s)"
            param = (username)
            user_id = query_execute(query, param)

            query = "SELECT LAST * FROM historical WHERE user_id = (%s)" 
            param = (user_id)
            pr_data = query_execute(query, param)
        except Exception as error:
            return jsonify({"message": f"Server error, please try again later. Error code: {error}"}), 500
        
        if pr_data:
            return jsonify({"message": "Data recieved", **pr_data}), 200
        else:
            return jsonify({"message": "Data not found"}), 404
    else:
        return jsonify({"message': 'Missing username parameter"}), 400