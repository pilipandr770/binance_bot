import time
import requests
import sqlite3
import pandas as pd
from datetime import datetime
import config

DATABASE = 'crypto_data.db'

# Функція для отримання поточної ціни з Binance
def get_current_price(symbol='BTCUSDT'):
    url = f'https://api.binance.com/api/v3/ticker/price'
    params = {'symbol': symbol}
    response = requests.get(url, params=params)
    return float(response.json()['price'])

# Функція для створення таблиці цін, якщо вона не існує
def create_price_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS btc_usdt (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        price REAL,
                        timestamp TEXT
                    )''')
    conn.commit()
    conn.close()

# Функція для запису ціни у базу
def record_price(price):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''INSERT INTO btc_usdt (price, timestamp) VALUES (?, ?)''', (price, timestamp))
    conn.commit()
    conn.close()

# Функція для розрахунку ковзної середньої
def calculate_ma(prices, period):
    return pd.Series(prices).rolling(window=period).mean().iloc[-1]

# Функція для контролю ордерів
def cancel_all_orders():
    print("Скасування всіх ордерів!")
    # Логіка для скасування всіх активних ордерів (симуляція, замініть на API для реальної торгівлі)

# Функція для виставлення ордерів
def place_order(direction, price, stop_loss, take_profit):
    print(f"Виставляємо ордери: {direction}, ціна: {price}, стоп-лосс: {stop_loss}, тейк-профіт: {take_profit}")
    # Логіка для виставлення ордерів (симуляція, замініть на API для реальної торгівлі)
    # Ви можете використовувати Binance API для виставлення ордерів

def trade():
    create_price_table()  # Створюємо таблицю, якщо вона не існує

    while True:
        # Отримуємо поточну ціну
        price = get_current_price()
        print(f"Поточна ціна: {price}")

        # Записуємо ціну у базу
        record_price(price)

        # Підключаємося до бази даних для отримання останніх 25 цін
        conn = sqlite3.connect(DATABASE)
        df = pd.read_sql_query("SELECT price, timestamp FROM btc_usdt ORDER BY timestamp DESC LIMIT 25", conn)
        conn.close()

        # Перевіряємо кількість записів
        if len(df) >= 25:
            df = df[::-1]  # Перевертаємо DataFrame, щоб найстаріші записи були зверху

            # Обчислюємо MA7 і MA25
            ma_7 = calculate_ma(df['price'], 7)
            ma_25 = calculate_ma(df['price'], 25)

            print(f"MA7: {ma_7}, MA25: {ma_25}")

            # Розраховуємо стоп-лосс і тейк-профіт
            stop_loss = price * (1 - config.STOP_LOSS_PERCENT / 100)  # Конфігурований стоп-лосс
            take_profit = price * (1 + config.TAKE_PROFIT_PERCENT / 100)  # Конфігурований тейк-профіт

            # Логіка для перевірки тренду і виставлення ордерів
            if ma_7 > ma_25:
                print("Тренд вгору, відкриваємо позицію на купівлю.")
                place_order("купити", price, stop_loss, take_profit)
            elif ma_7 < ma_25:
                print("Тренд вниз, відкриваємо позицію на продаж.")
                place_order("продати", price, stop_loss, take_profit)
        else:
            print(f"Недостатньо даних для обчислення MA. Маємо {len(df)} записів.")

        # Чекаємо 1 секунду перед наступним сигналом
        time.sleep(1)

# Основна точка входу
if __name__ == "__main__":
    try:
        trade()
    except KeyboardInterrupt:
        print("Бот зупинено.")
