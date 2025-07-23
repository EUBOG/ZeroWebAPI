from flask import Flask, render_template
import requests
import cloudscraper  # pip install cloudscraper
import random

app = Flask(__name__)

# Локальные цитаты на случай сбоев
backup_quotes = [
    {"quote": "Будь тем, кто ты есть.", "author": "Бернард Барух"},
    {"quote": "Успех — это идти от неудачи к неудаче.", "author": "Уинстон Черчилль"},
    {"quote": "Жизнь — это то, что с тобой происходит.", "author": "Джон Леннон"},
]

def get_random_backup():
    return random.choice(backup_quotes)

def get_zenquote():
    try:
        response = requests.get("https://zenquotes.io/api/random", timeout=5)
        if response.status_code == 200:
            data = response.json()
            # Проверяем, что это действительно JSON с цитатой
            if isinstance(data, list) and 'q' in data[0]:
                return {"quote": data[0]['q'], "author": data[0]['a']}
    except Exception as e:
        print("Ошибка ZenQuotes:", e)
    return None

def get_quoteslate_quote():
    try:
        scraper = cloudscraper.create_scraper()
        response = scraper.get("https://quoteslate.vercel.app/api/quotes/random", timeout=10)
        if response.status_code == 200:
            data = response.json()
            # Убедимся, что мы извлекаем поля правильно
            return {"quote": data["quote"], "author": data["author"]}
    except Exception as e:
        print("Ошибка Quoteslate:", e)
    return None

@app.route('/')
def index():
    # Первая цитата — ZenQuotes (с fallback)
    quote1 = get_zenquote() or get_random_backup()

    # Вторая цитата — Quoteslate (с fallback)
    raw_quote2 = get_quoteslate_quote()  # Это словарь: {"quote": "...", "author": "..."}
    quote2 = raw_quote2 or get_random_backup()

    # Гарантируем разные цитаты
    while quote2['quote'] == quote1['quote']:
        quote2 = get_random_backup()

    return render_template('index.html', quote1=quote1, quote2=quote2)

if __name__ == '__main__':
    app.run(debug=True)