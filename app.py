import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

WORDPRESS_WEBHOOK_URL = "https://caesarboxing.ru/wp-admin/admin-ajax.php?action=handle_wheel_lead"

import json

@app.route("/webhook", methods=["POST"])
def handle_lead():
    data = request.json

    if not data or "phone" not in data or "name" not in data:
        return jsonify({"success": False, "message": "Некорректные данные"}), 400

    print(f"🔥 Отправка в WordPress: {json.dumps(data, indent=2, ensure_ascii=False)}")

    # Отправка данных в WordPress
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(WORDPRESS_WEBHOOK_URL, json=data, headers=headers)
        print(f"📩 Ответ WordPress: {response.status_code}, {response.text}")

        if response.status_code == 200:
            return jsonify({"success": True, "message": "Лид успешно отправлен в WordPress"})
        else:
            return jsonify({"success": False, "message": "Ошибка при отправке в WordPress"}), 500
    except Exception as e:
        print(f"⚠️ Ошибка: {e}")
        return jsonify({"success": False, "message": "Ошибка на сервере"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

