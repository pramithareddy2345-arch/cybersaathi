
from flask import Flask, render_template, request, jsonify, redirect, url_for
@app.route("/")
def home():
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
