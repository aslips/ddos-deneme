import requests
import threading
import time
import random


base_url = "http://127.0.0.1:5002"


endpoints = ["/", "/api", "/form", "/data", "/profile"]

# toplam istek ve thread sayısı
number_of_requests = 1000
threads_count = 10

# her threadin göndereceği istek
def send_request():
    try:
        endpoint = random.choice(endpoints)
        full_url = base_url + endpoint

        fake_ip = f"10.0.0.{random.randint(1, 254)}"
        headers = {
            "X-Traffic-Type": "DDoS",
            "X-Forwarded-For": fake_ip
        }

        response = requests.get(full_url, headers=headers)
        print(f"[✓] DDoS isteği – {full_url} – IP: {fake_ip} – Kod: {response.status_code}")
    except Exception as e:
        print(f"[X] Hata: {e}")

def attack():
    for _ in range(int(number_of_requests / threads_count)):
        send_request()

# Süreyi ölç
start_time = time.time()

# Thread’leri başlat
threads = []
for i in range(threads_count):
    t = threading.Thread(target=attack)
    t.start()
    threads.append(t)

# Bitmelerini bekle
for t in threads:
    t.join()

end_time = time.time()
print(f"\n Toplam süre: {round(end_time - start_time, 2)} saniye")
