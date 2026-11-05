from flask import Flask, request, jsonify

import sqlite3
import uuid
from datetime import datetime

app = Flask(__name__)
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response
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
    # ==========================================
# CYBERSAATHI - ADVANCED CYBER SECURITY FEATURES
# ==========================================

import re
import ipaddress
from urllib.parse import urlparse


# 1. PHISHING URL DETECTOR
@app.route("/api/phishing-check", methods=["POST"])
def phishing_check():
    data = request.get_json(silent=True) or {}
    url = data.get("url", "").strip()

    if not url or len(url) > 2048:
        return jsonify({"error": "Please enter a valid URL."}), 400

    candidate = url if "://" in url else "https://" + url

    try:
        parsed = urlparse(candidate)
        host = parsed.hostname or ""

        if parsed.scheme not in ("http", "https") or not host:
            raise ValueError()

        risk = 0
        reasons = []

        if parsed.scheme == "http":
            risk += 1
            reasons.append("Website does not use HTTPS.")

        if "@" in parsed.netloc:
            risk += 2
            reasons.append("URL contains unusual login information.")

        try:
            ipaddress.ip_address(host)
            risk += 2
            reasons.append("URL uses an IP address instead of a domain.")
        except ValueError:
            pass

        if host.startswith("xn--") or ".xn--" in host:
            risk += 2
            reasons.append("Domain contains encoded characters.")

        if len(host.split(".")) > 4:
            risk += 1
            reasons.append("Domain has unusually many subdomains.")

        suspicious_words = [
            "verify", "login", "secure", "free",
            "account-update", "gift", "claim",
            "password", "banking"
        ]

        if any(word in candidate.lower() for word in suspicious_words):
            risk += 1
            reasons.append("URL contains commonly abused words.")

        if risk >= 3:
            result = "Suspicious"
        elif risk >= 1:
            result = "Needs Caution"
        else:
            result = "No obvious warning signs"

        return jsonify({
            "status": "success",
            "result": result,
            "risk_score": min(risk, 6),
            "warnings": reasons,
            "message": "This is a basic heuristic check, not a guarantee that a website is safe."
        })

    except ValueError:
        return jsonify({"error": "Invalid URL format."}), 400


# 2. SCAM MESSAGE DETECTOR
@app.route("/api/scam-check", methods=["POST"])
def scam_check():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()

    if not message or len(message) > 5000:
        return jsonify({"error": "Enter a message under 5000 characters."}), 400

    keywords = [
        "urgent payment", "send otp", "share otp",
        "account blocked", "claim your prize",
        "you won", "click this link",
        "bank details", "send money",
        "limited time", "verify your account",
        "upi pin", "remote access"
    ]

    found = [word for word in keywords if word in message.lower()]

    risk = len(found)

    if risk >= 3:
        result = "High Risk"
    elif risk >= 1:
        result = "Potentially Suspicious"
    else:
        result = "No obvious scam indicators"

    return jsonify({
        "status": "success",
        "result": result,
        "risk_score": min(risk, 10),
        "warning_signs": found,
        "advice": "Never share OTPs, passwords or UPI PINs. Verify requests through official channels."
    })


# 3. CYBER SAFETY TIPS
@app.route("/api/cyber-tips", methods=["GET"])
def cyber_tips():
    tips = [
        "Never share your OTP with anyone.",
        "Use strong and unique passwords.",
        "Enable two-factor authentication.",
        "Avoid clicking unknown links.",
        "Never share your UPI PIN.",
        "Keep your applications updated.",
        "Avoid public Wi-Fi for banking.",
        "Check website addresses before logging in.",
        "Do not download unknown attachments.",
        "Report cyber fraud immediately."
    ]

    return jsonify({
        "status": "success",
        "tips": tips
    })


# 4. CYBER SAFETY ASSISTANT
@app.route("/api/cyber-assistant", methods=["POST"])
def cyber_assistant():
    data = request.get_json(silent=True) or {}
    question = data.get("question", "").strip().lower()

    if not question or len(question) > 2000:
        return jsonify({"error": "Please enter a question."}), 400

    responses = {
        "otp": "Never share your OTP with anyone, including people claiming to be bank officials.",
        "phishing": "Phishing is an online trick used to steal personal information through fake websites or messages.",
        "password": "Use long, unique passwords and enable two-factor authentication.",
        "upi": "Never share your UPI PIN. You do not need to enter a PIN to receive money.",
        "fraud": "If you experience cyber financial fraud in India, contact 1930 immediately and report it at cybercrime.gov.in.",
        "hacked": "Secure your accounts using a trusted device, change compromised passwords and enable two-factor authentication."
    }

    answer = (
        next((value for key, value in responses.items() if key in question),
             "Stay alert online. Never share sensitive information, avoid unknown links and verify suspicious requests through official sources.")
    )

    return jsonify({
        "status": "success",
        "assistant": "CyberSaathi AI Assistant",
        "answer": answer,
        "notice": "This is a basic rule-based assistant, not a connected AI model."
    })


# 5. CYBERCRIME REPORTING GUIDANCE
@app.route("/api/cyber-help", methods=["GET"])
def cyber_help():
    return jsonify({
        "status": "success",
        "helpline": "1930",
        "portal": "https://cybercrime.gov.in/",
        "instructions": [
            "Contact 1930 immediately if you experience financial cyber fraud.",
            "Visit the official National Cyber Crime Reporting Portal.",
            "Keep transaction IDs and relevant evidence.",
            "Never share your OTP, password or UPI PIN."
        ]
    })

    create_database()
    app.run(host="0.0.0.0", port=5000)
