
from flask import Flask, render_template, request, jsonify, redirect, url_for
@app.route("/")
    return render_template("index.html")
import os

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY", "cybersaathi-secret-key")
@app.route("/api")
def api():
    return jsonify({
        "service": "CyberSaathi API",
        "status": "ok"
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    

# ===== CYBERSAATHI ADVANCED FEATURES =====

import ipaddress
from urllib.parse import urlparse


# 1. PHISHING URL CHECKER
@app.route("/api/phishing-check", methods=["POST"])
def phishing_check():
    data = request.get_json(silent=True) or {}
    url = data.get("url", "").strip()

    if not url or len(url) > 2048:
        return jsonify({"error": "Enter a valid URL"}), 400

    try:
        parsed = urlparse(
            url if "://" in url else "https://" + url
        )
        host = parsed.hostname or ""

        if parsed.scheme not in ("http", "https") or not host:
            return jsonify({"error": "Invalid URL"}), 400

        risk = 0
        warnings = []

        if parsed.scheme == "http":
            risk += 1
            warnings.append("HTTPS is not enabled")

        if "@" in parsed.netloc:
            risk += 2
            warnings.append("Unusual URL structure")

        try:
            ipaddress.ip_address(host)
            risk += 2
            warnings.append("Uses an IP address instead of a domain")
        except ValueError:
            pass

        if len(host.split(".")) > 4:
            risk += 1
            warnings.append("Unusual number of subdomains")

        result = (
            "Suspicious" if risk >= 3
            else "Needs Caution" if risk >= 1
            else "No obvious warning signs"
        )

        return jsonify({
            "status": "success",
            "result": result,
            "risk_score": risk,
            "warnings": warnings,
            "notice": "This basic check cannot guarantee website safety."
        })

    except ValueError:
        return jsonify({"error": "Invalid URL"}), 400


# 2. SCAM MESSAGE DETECTOR
@app.route("/api/scam-check", methods=["POST"])
def scam_check():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()

    if not message or len(message) > 5000:
        return jsonify({"error": "Enter a message under 5000 characters"}), 400

    keywords = [
        "urgent payment", "send otp", "share otp",
        "account blocked", "claim your prize",
        "you won", "click this link",
        "send money", "upi pin",
        "verify your account"
    ]

    found = [
        word for word in keywords
        if word in message.lower()
    ]

    risk = len(found)

    result = (
        "High Risk" if risk >= 3
        else "Potentially Suspicious" if risk >= 1
        else "No obvious scam indicators"
    )

    return jsonify({
        "status": "success",
        "result": result,
        "risk_score": risk,
        "warning_signs": found,
        "advice": "Never share OTPs, passwords or UPI PINs."
    })


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

# ===== END CYBERSAATHI FEATURES =====

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
