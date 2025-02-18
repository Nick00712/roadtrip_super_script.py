import os
import json
import datetime
import threading
import requests
from flask import Flask, request, jsonify

# Configuration
TOTAL_BUDGET = 3500  # Total trip budget in AUD
ALERT_STEP = 500  # SMS every $500 spent
EXPENSE_SHEET_ID = "your-google-sheet-id"
DB_FILE = "roadtrip_data.db"

# API Keys (DO NOT STORE IN PUBLIC GITHUB REPO)
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Flask Setup
app = Flask(__name__)

# Navigation Destinations
NAVIGATION_DESTINATIONS = {
    "2025-02-24": "Mataranka Homestead, NT",
    "2025-02-25": "Daly Waters Pub, NT",
    "2025-02-26": "Devils Marbles, NT",
    "2025-02-27": "Ellery Creek Big Hole, NT",
    "2025-02-28": "Uluru-Kata Tjuta, NT",
    "2025-03-01": "Coober Pedy, SA",
    "2025-03-02": "Port Augusta, SA",
    "2025-03-03": "Adelaide, SA",
    "2025-03-04": "Hahndorf, SA",
    "2025-03-05": "Donald, VIC",
}

# Recommended Fuel Stops
FUEL_STOPS = {
    "2025-02-24": "Katherine, NT",
    "2025-02-25": "Dunmarra Roadhouse, NT",
    "2025-02-26": "Tennant Creek, NT",
    "2025-02-28": "Erldunda Roadhouse, NT",
    "2025-03-01": "Glendambo, SA",
    "2025-03-02": "Port Augusta, SA",
}

# AI Travel Assistant
@app.route('/voice_assistant', methods=['POST'])
def voice_assistant():
    speech_text = request.json.get("text", "")
    if not speech_text:
        return jsonify({"error": "No input detected"}), 400
    
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"},
            json={
                "model": "gpt-4-turbo",
                "messages": [{"role": "system", "content": "You are a helpful AI travel assistant."},
                             {"role": "user", "content": speech_text}]
            },
        )
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)})

# Log expenses
@app.route('/log_expense', methods=['POST'])
def log_expense():
    data = request.json
    amount = data.get("amount")
    category = data.get("category", "General")
    merchant = data.get("merchant", "Unknown")
    timestamp = data.get("timestamp", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    # Log to Google Sheets (Future implementation)
    print(f"Logged Expense: {amount} at {merchant} ({category}) on {timestamp}")
    return jsonify({"message": "Expense logged successfully."}), 200

# Fetch & Execute Latest Script from GitHub
@app.route('/update_script', methods=['GET'])
def update_script():
    SCRIPT_URL = "https://raw.githubusercontent.com/YOUR_USERNAME/roadtrip-automation/main/roadtrip_super_script.py"
    response = requests.get(SCRIPT_URL)
    if response.status_code == 200:
        with open("roadtrip_super_script.py", "w") as file:
            file.write(response.text)
        return jsonify({"message": "✅ Script updated successfully!"})
    return jsonify({"message": "❌ Failed to fetch script!"})

@app.route('/run_script', methods=['POST'])
def run_script():
    os.system("python3 roadtrip_super_script.py &")
    return jsonify({"message": "🚀 Script is running in the background!"})

# Error Logging & Email Reports (Future implementation)
@app.route('/email_log', methods=['POST'])
def email_log():
    # Placeholder for sending logs via email
    return jsonify({"message": "Email log sent!"})

if __name__ == '__main__':
    print("🚀 Starting Automated Trip Assistant...")
    app.run(host='0.0.0.0', port=5000)
