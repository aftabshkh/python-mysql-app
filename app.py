# app.py
from flask import Flask, request, jsonify
import mysql.connector
import os

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = mysql.connector.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        user=os.environ.get('DB_USER', 'root'),
        password=os.environ.get('DB_PASSWORD', 'password'),
        database=os.environ.get('DB_NAME', 'test_db')
    )
    return conn

@app.route('/add', methods=['POST'])
def add_user():
    data = request.json
    name = data['name']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name) VALUES (%s)", (name,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "User added!"}), 201

@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(users)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
