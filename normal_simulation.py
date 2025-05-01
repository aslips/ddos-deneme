import requests
import time
import random


base_url = "http://127.0.0.1:5002"


endpoints = ["/", "/login", "/dashboard", "/profile", "/data", "/form"]

# normal kullanıcı gibi davransaniyede 1 istek gönder
for i in range(100):
    try:
       
        endpoint = random.choice(endpoints)
        full_url = base_url + endpoint

        #rastgele sahte ip
        fake_ip = f"192.168.1.{random.randint(1, 254)}"

       
        headers = {
            "X-Traffic-Type": "Normal",
            "X-Forwarded-For": fake_ip
        }

       
        response = requests.get(full_url, headers=headers)
        print(f"[✓] Normal istek gönderildi – {full_url} – IP: {fake_ip} – Kod: {response.status_code}")

    except Exception as e:
        print(f"[X] Hata: {e}")

    time.sleep(1)  # 1 saniyede bir
