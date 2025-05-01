from flask import Flask, request, jsonify, render_template
import time
import csv
from datetime import datetime
import os
import joblib
import pandas as pd

print("Flask sunucusu başlatılıyor...")

app = Flask(__name__)
log_file = 'loglar.csv'
model = joblib.load("ddos_model.pkl")

columns = ['timestamp', 'ip', 'endpoint', 'response_time_ms', 'label', 'hour', 'ip_class', 'user_agent_type']
if not os.path.exists(log_file):
    with open(log_file, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(columns)

def classify_ip(ip):
    try:
        first = int(ip.split(".")[0])
        if 0 <= first <= 126:
            return "A"
        elif 128 <= first <= 191:
            return "B"
        elif 192 <= first <= 223:
            return "C"
        elif 224 <= first <= 239:
            return "D"
        else:
            return "E"
    except:
        return "Unknown"

def process_request(endpoint_path="/"):
    start = time.time()
    response = "Sunucu çalışıyor!"
    end = time.time()
    response_time = round((end - start) * 1000, 2)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    hour = datetime.now().hour

    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    endpoint = endpoint_path
    label = request.headers.get("X-Traffic-Type", "DDoS")

    user_agent = request.headers.get("User-Agent", "Unknown").lower()
    user_agent_type = "CLI" if "python" in user_agent or "curl" in user_agent else "Browser"
    ip_class = classify_ip(ip)

    #model tahmini
    sample = {
        "response_time_ms": response_time,
        "endpoint": endpoint,
        "hour": hour,
        "ip_class": ip_class,
        "user_agent_type": user_agent_type
    }

    df = pd.DataFrame([sample])
    df = pd.get_dummies(df)

    model_features = model.feature_names_in_
    for col in model_features:
        if col not in df.columns:
            df[col] = 0
    df = df[model_features]

    prediction = model.predict(df)[0]

    # Logla
    with open(log_file, mode='a', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow([timestamp, ip, endpoint, response_time, label, hour, ip_class, user_agent_type])

    print(f"📥 Loglandı: {ip} {endpoint} [{response_time} ms] - {label}")
    print(f"🤖 Tahmin edilen trafik türü: {prediction}")

    return jsonify({
        "message": response,
        "ip": ip,
        "endpoint": endpoint,
        "model_prediction": prediction,
        "logged_label": label
    })

@app.route("/")
def home():
    return process_request("/")

@app.route('/<path:any_path>')
def catch_all(any_path):
    return process_request(f"/{any_path}")


@app.route("/form", methods=["GET"])
def show_form():
    return render_template("form.html")

@app.route("/tahmin", methods=["POST"])
def predict_from_form():
    ip = request.form["ip"]
    endpoint = request.form["endpoint"]
    response_time = float(request.form["response_time"])
    hour = int(request.form["hour"])
    user_agent_type = request.form["user_agent_type"]
    ip_class = classify_ip(ip)

    row = [[hour, response_time, ip_class, user_agent_type]]
    df = pd.DataFrame(row, columns=["hour", "response_time_ms", "ip_class", "user_agent_type"])
    df = pd.get_dummies(df)

    expected_cols = model.feature_names_in_
    for col in expected_cols:
        if col not in df.columns:
            df[col] = 0
    df = df[expected_cols]

    prediction = model.predict(df)[0]
    return render_template("form.html", prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True, port=5002)
