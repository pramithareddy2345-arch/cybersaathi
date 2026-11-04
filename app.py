from flask import Flask, request, jsonify
import sqlite3
import uuid
from datetime import datetime

app = Flask(__name__)
DATABASE = "cybersaathi.db"


def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def create_database():
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reference TEXT UNIQUE,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            incident_date TEXT,
            created_at TEXT NOT NULL
        )
    """)
    db.commit()
    db.close()


@app.route("/")
def home():
    return jsonify({
        "service": "CyberSaathi API",
        "status": "running"
    })


@app.route("/api/complaints", methods=["POST"])
def submit_complaint():
    data = request.get_json(silent=True) or {}

    category = data.get("category", "").strip()
    description = data.get("description", "").strip()
    incident_date = data.get("incident_date", "")

    if not category or not description:
        return jsonify({
            "error": "Category and description are required"
        }), 400

    reference = "CS-" + uuid.uuid4().hex[:8].upper()

    db = get_db()
    db.execute("""
        INSERT INTO complaints
        (reference, category, description, incident_date, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (
        reference,
        category,
        description,
        incident_date,
        datetime.now().isoformat()
    ))
    db.commit()
    db.close()

    return jsonify({
        "message": "Demo complaint saved successfully",
        "reference": reference,
        "official_police_submission": False
    }), 201


@app.route("/api/complaints/<reference>")
def track_complaint(reference):
    db = get_db()
    complaint = db.execute(
        "SELECT reference, category, created_at FROM complaints WHERE reference = ?",
        (reference,)
    ).fetchone()
    db.close()

    if complaint is None:
        return jsonify({"error": "Complaint not found"}), 404

    return jsonify(dict(complaint))


if __name__ == "__main__":
    create_database()
    app.run(host="0.0.0.0", port=5000)
