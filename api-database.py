import psycopg2
from flask import Flask, request, jsonify

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