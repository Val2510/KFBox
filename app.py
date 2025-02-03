import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

WORDPRESS_WEBHOOK_URL = "https://caesarboxing.ru/wp-admin/admin-ajax.php?action=handle_wheel_lead"

@app.route("/webhook", methods=["POST"])
def handle_lead():
    data = request.json

    print("📩 Полученные данные во Flask:", data)  # Логируем данные

    if not data or "phone" not in data or "name" not in data:
        print("🚨 Ошибка: Некорректные данные")
        return jsonify({"success": False, "message": "Некорректные данные"}), 400

    print(f"✅ Лид принят: {data}")

    # Отправка данных в WordPress
    try:
        response = requests.post(WORDPRESS_WEBHOOK_URL, data=data)
        print(f"📤 Отправка в WordPress: {response.status_code}, {response.text}")

        if response.status_code == 200:
            return jsonify({"success": True, "message": "Лид успешно отправлен в WordPress"})
        else:
            print("❌ Ошибка при отправке в WordPress!")
            return jsonify({"success": False, "message": "Ошибка при отправке в WordPress"}), 500
    except Exception as e:
        print(f"⚠️ Ошибка на сервере Flask: {e}")
        return jsonify({"success": False, "message": "Ошибка на сервере"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

