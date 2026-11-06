
from flask import Flask, render_template, request, jsonify
import os
import ipaddress
import sqlite3
import uuid
from urllib.parse import urlparse
from datetime import datetime

# Initialize Flask only once
app = Flask(
    __name__,
    template_folder=os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "templates"
    )
)

DATABASE = "cybersaathi.db"


# DATABASE
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


# HOME PAGE
@app.route("/")
def home():
    return render_template("index.html")


# API STATUS
@app.route("/api")
def api():
    return jsonify({
        "service": "CyberSaathi API",
        "status": "ok"
    })


# 1. PHISHING URL CHECKER
from urllib.parse import urlparse

def scan_url(url):
    url = url.strip()

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    hostname = (urlparse(url).hostname or "").lower()

    trusted_domains = [
        "youtube.com",
        "google.com",
        "microsoft.com",
        "wikipedia.org"
    ]

    for domain in trusted_domains:
        if hostname == domain or hostname.endswith("." + domain):
            return {
                "status": "Safe",
                "message": "No known warning signs detected."
            }

    # Continue with your existing suspicious URL checks here.
    return {
        "status": "Needs Review",
        "message": "This URL requires further security checks."
    }
            


# 3. CYBER SAFETY TIPS
@app.route("/api/cyber-tips", methods=["GET"])
def cyber_tips():
    return jsonify({
        "status": "success",
        "tips": [
            "Never share your OTP.",
            "Use strong and unique passwords.",
            "Enable two-factor authentication.",
            "Avoid unknown links.",
            "Never share your UPI PIN.",
            "Keep applications updated.",
            "Avoid banking on public Wi-Fi.",
            "Verify website addresses.",
            "Avoid unknown attachments.",
            "Report cyber fraud immediately."
        ]
    })


# 4. CYBER SAFETY ASSISTANT
@app.route("/api/cyber-assistant", methods=["POST"])
def cyber_assistant():
    data = request.get_json(silent=True) or {}
    question = data.get("question", "").strip().lower()

    if not question or len(question) > 2000:
        return jsonify({"error": "Enter your question"}), 400

    answers = {
        "otp": "Never share your OTP with anyone.",
        "phishing": "Phishing uses deceptive messages and websites to steal information.",
        "password": "Use unique passwords and enable two-factor authentication.",
        "upi": "Never share your UPI PIN. You do not need a PIN to receive money.",
        "fraud": "In India, call 1930 immediately for financial cyber fraud and report it at cybercrime.gov.in.",
        "hacked": "Secure your accounts from a trusted device, change compromised passwords and enable two-factor authentication."
    }

    answer = next(
        (value for key, value in answers.items() if key in question),
        "Stay safe online. Avoid unknown links and never share sensitive information."
    )

    return jsonify({
        "status": "success",
        "assistant": "CyberSaathi",
        "answer": answer,
        "notice": "This is a basic rule-based assistant."
    })


# 5. CYBERCRIME HELP
@app.route("/api/cyber-help", methods=["GET"])
def cyber_help():
    return jsonify({
        "status": "success",
        "helpline": "1930",
        "portal": "https://cybercrime.gov.in/",
        "instructions": [
            "Call 1930 immediately for financial cyber fraud.",
            "Visit the official cybercrime reporting portal.",
            "Keep transaction IDs and relevant evidence.",
            "Never share your OTP or UPI PIN."
        ]
    })


# 6. SUBMIT COMPLAINT
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


# 7. TRACK COMPLAINT
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


# CREATE DATABASE WHEN THE APP STARTS
create_database()


# START SERVER
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    
