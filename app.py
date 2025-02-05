from urllib import response
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Настройки WordPress API
WP_SITE_URL = "https://caesarboxing.ru/"
WP_API_ENDPOINT = f"{WP_SITE_URL}/wp-json/wp/v2/leads"  # URL для кастомного типа записей
WP_USERNAME = "boxing79admin"
WP_PASSWORD = "#fNb)FEInTe9yN7Cqs"  # Используйте Application Passwords в WordPress

@app.route('/submit_lead', methods=['POST'])
def submit_lead():
    try:
        # Получаем данные из запроса
        data = request.json
        name = data.get("name")
        phone = data.get("phone")
        prize = data.get("prize")

        if not all([name, phone]):
            return jsonify({"error": "Missing required fields"}), 400

        # Создаем новую запись в WordPress
        wp_post_data = {
            "title": name,  # Имя лида будет заголовком
            "status": "publish",  # Можно сменить на "draft", если не хотите публиковать сразу
            "meta": {
                "phone": phone,
                "prize": prize
            }
        }

        # Отправляем запрос в WordPress
        requests.post("http://127.0.0.1:5000/submit_lead", json=wp_post_data, auth=(WP_USERNAME, WP_PASSWORD))


        if response.status_code == 201:
            return jsonify({"message": "Lead successfully created"}), 201
        else:
            return jsonify({"error": "Failed to create lead", "details": response.json()}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)



