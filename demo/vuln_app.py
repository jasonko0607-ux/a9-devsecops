import sqlite3
import subprocess

from flask import Flask, request

app = Flask(__name__)


@app.route("/user")
def get_user():
    name = request.args.get("name", "")
    conn = sqlite3.connect("demo.db")
    query = f"SELECT * FROM users WHERE name = '{name}'"
    rows = conn.execute(query).fetchall()
    return {"rows": rows}


@app.route("/ping")
def ping():
    host = request.args.get("host", "")
    result = subprocess.run(f"ping -c 1 {host}", shell=True,
                            capture_output=True, text=True)
    return {"output": result.stdout}
