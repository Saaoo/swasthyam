from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import os

app = Flask(__name__)

DATABASE = 'swasthyam.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    # Create HealthProfile table if it doesn't exist
    cur.execute('''
    CREATE TABLE IF NOT EXISTS HealthProfile (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        weight REAL,
        height REAL,
        pulse_rate INTEGER,
        blood_pressure TEXT,
        stress_levels TEXT,
        weight_management_goals TEXT,
        health_conditions TEXT
    )
    ''')
    # Create ChatMessages table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS ChatMessages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        message TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
    conn.close()

# Initialize the database tables on server start
init_db()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if request.method == "POST":
        weight = request.form.get("weight")
        height = request.form.get("height")
        pulse_rate = request.form.get("pulse_rate")
        blood_pressure = request.form.get("blood_pressure")
        stress_levels = request.form.get("stress_levels")
        weight_management_goals = request.form.get("weight_management_goals")
        health_conditions = request.form.get("health_conditions")
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO HealthProfile (weight, height, pulse_rate, blood_pressure, stress_levels, weight_management_goals, health_conditions)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (weight, height, pulse_rate, blood_pressure, stress_levels, weight_management_goals, health_conditions))
        conn.commit()
        conn.close()
        return redirect(url_for('profile'))
    else:
        # For demonstration, load the most recent profile entry (if available)
        conn = get_db_connection()
        profile = conn.execute('SELECT * FROM HealthProfile ORDER BY id DESC LIMIT 1').fetchone()
        conn.close()
        return render_template("profile.html", profile=profile)

@app.route("/customization")
def customization():
    # For demo purposes, we simulate AI customization by outputting dummy data.
    # In a real application, you would integrate an AI module.
    conn = get_db_connection()
    profile = conn.execute('SELECT * FROM HealthProfile ORDER BY id DESC LIMIT 1').fetchone()
    conn.close()
    
    if profile:
        # Customize routines based on profile data
        yoga_routine = "Sun Salutation Series with deep breathing—recommended for your weight of " + str(profile["weight"]) + " kg."
        diet_plan = "A balanced diet rich in fruits, vegetables, and lean proteins suited for your height of " + str(profile["height"]) + " cm."
    else:
        yoga_routine = "General yoga routine: Focus on flexibility and strength."
        diet_plan = "General diet: Stay hydrated and maintain balanced nutrition."
    
    return render_template("customization.html", yoga_routine=yoga_routine, diet_plan=diet_plan)

@app.route("/wellness")
def wellness():
    return render_template("wellness.html")

@app.route("/community")
def community():
    # Retrieve the latest 20 chat messages
    conn = get_db_connection()
    messages = conn.execute('SELECT * FROM ChatMessages ORDER BY timestamp DESC LIMIT 20').fetchall()
    conn.close()
    return render_template("community.html", messages=messages)

@app.route("/send_message", methods=["POST"])
def send_message():
    username = request.form.get("username", "Anonymous")
    message = request.form.get("message")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO ChatMessages (username, message) VALUES (?, ?)", (username, message))
    conn.commit()
    conn.close()
    return redirect(url_for('community'))

@app.route("/get_messages")
def get_messages():
    # Provide chat messages as JSON for the AJAX caller
    conn = get_db_connection()
    messages = conn.execute("SELECT * FROM ChatMessages ORDER BY timestamp DESC LIMIT 20").fetchall()
    conn.close()
    messages_list = []
    for row in messages:
        messages_list.append({
            "username": row["username"],
            "message": row["message"],
            "timestamp": row["timestamp"]
        })
    return jsonify(messages_list)

if __name__ == '__main__':
    # Run the server with an ad hoc self-signed SSL certificate for HTTPS support.
    app.run(ssl_context='adhoc', debug=True)
