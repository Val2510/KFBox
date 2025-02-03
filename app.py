import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# URL для отправки лида в WordPress
WORDPRESS_WEBHOOK_URL = "https://caesarboxing.ru/wp-admin/admin-ajax.php?action=handle_wheel_lead"

# Главная страница (проверка сервера)
@app.route('/', methods=['GET'])
def home():
    return "Flask-сервер запущен и готов принимать запросы", 200

# Обработчик для получения лида
@app.route("/webhook", methods=["POST"])
def handle_lead():
    data = request.get_json()  # Читаем JSON-данные из запроса

    # Проверка, что все обязательные поля заполнены
    required_fields = ["name", "phone", "prize"]
    missing_fields = [field for field in required_fields if field not in data or not data[field]]

    if missing_fields:
        return jsonify({
            "success": False,
            "message": f"Отсутствуют обязательные поля: {', '.join(missing_fields)}"
        }), 400

    print(f"📩 Получены данные лида: {data}")

    try:
        # Отправляем запрос в WordPress
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.post(WORDPRESS_WEBHOOK_URL, data=data, headers=headers)
        response_json = response.json()  # Пробуем обработать ответ как JSON

        print(f"✅ Ответ WordPress: {response.status_code}, {response.text}")

        if response.status_code == 200 and response_json.get("success"):
            return jsonify({"success": True, "message": "Лид успешно отправлен в WordPress"})
        else:
            return jsonify({
                "success": False,
                "message": f"Ошибка при отправке в WordPress: {response_json.get('message', 'Неизвестная ошибка')}"
            }), 500

    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка запроса к WordPress: {e}")
        return jsonify({"success": False, "message": "Ошибка при соединении с WordPress"}), 500

    except ValueError:
        print(f"❌ Ошибка парсинга ответа от WordPress: {response.text}")
        return jsonify({"success": False, "message": "Некорректный ответ от WordPress"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)


