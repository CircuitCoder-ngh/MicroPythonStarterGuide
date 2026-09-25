# Send a push notification to your phone with ntfy.sh
import requests
import secrets
import wifi

wifi.connect()

response = requests.post(
    "https://ntfy.sh/" + secrets.NTFY_TOPIC,
    data="Hello from my ESP32!",
)
print("Status code:", response.status_code)   # 200 means it was sent
response.close()
