from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

DB = "database.db"

def connect_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

# CREATE TABLE
def init_db():
    conn = connect_db()
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        password TEXT,
        is_vip INTEGER DEFAULT 0
    )
    """)
    conn.commit()
    conn.close()

init_db()

# REGISTER
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    conn = connect_db()
    c = conn.cursor()

    try:
        c.execute("INSERT INTO users (email, password) VALUES (?, ?)",
                  (data["email"], data["password"]))
        conn.commit()
        return jsonify({"message": "Account created"})
    except:
        return jsonify({"message": "User already exists"})

# LOGIN
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    conn = connect_db()
    c = conn.cursor()

    user = c.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (data["email"], data["password"])
    ).fetchone()

    if user:
        return jsonify({
            "message": "Login successful",
            "vip": user["is_vip"]
        })
    else:
        return jsonify({"message": "Invalid login"})

# SET VIP (we’ll connect to Mpesa later)
@app.route("/make_vip", methods=["POST"])
def make_vip():
    data = request.json
    conn = connect_db()
    c = conn.cursor()

    c.execute("UPDATE users SET is_vip=1 WHERE email=?", (data["email"],))
    conn.commit()

    return jsonify({"message": "User upgraded to VIP"})

app.run(host="0.0.0.0", port=5000)
