from flask import Flask, request, jsonify
import requests
import logging

app = Flask(__name__)

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# URL WordPress API
WORDPRESS_API_URL = "https://caesarboxing.ru/wp-admin/admin-ajax.php?action=handle_wheel_lead"

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    try:
        # Получаем данные из запроса
        data = request.json
        if not data:
            return jsonify({"error": "Пустой запрос"}), 400
        
        logging.info(f"Получены данные: {data}")

        # Формируем JSON для WordPress
        payload = {
            "name": data.get("name", ""),
            "phone": data.get("phone", ""),
            "prize": data.get("prize", ""),
            "utm_source": data.get("utm_source", ""),
            "utm_medium": data.get("utm_medium", ""),
            "utm_campaign": data.get("utm_campaign", ""),
            "utm_content": data.get("utm_content", "колесо фортуны"),
            "utm_term": data.get("utm_term", ""),
        }

        # Отправляем лид в WordPress
        response = requests.post(WORDPRESS_API_URL, data=payload)
        
        # Логируем ответ WordPress
        logging.info(f"Ответ WordPress: {response.status_code}, {response.text}")

        # Проверяем ответ
        if response.status_code == 200:
            return jsonify({"success": True, "message": "Лид успешно отправлен"})
        else:
            return jsonify({"success": False, "message": "Ошибка при отправке лида"}), response.status_code

    except Exception as e:
        logging.error(f"Ошибка: {e}")
        return jsonify({"error": "Ошибка сервера"}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
