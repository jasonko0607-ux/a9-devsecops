import re
import sqlite3
import subprocess

from flask import Flask, request

app = Flask(__name__)
HOST_PATTERN = re.compile(r"[A-Za-z0-9.-]{1,253}")


@app.route("/user")
def get_user():
    name = request.args.get("name", "")
    conn = sqlite3.connect("demo.db")
    rows = conn.execute(
        "SELECT * FROM users WHERE name = ?", (name,)
    ).fetchall()
    return {"rows": rows}


@app.route("/ping")
def ping():
    host = request.args.get("host", "")
    if not HOST_PATTERN.fullmatch(host):
        return {"error": "invalid host"}, 400
    result = subprocess.run(["ping", "-c", "1", host],
                            capture_output=True, text=True)
    return {"output": result.stdout}
