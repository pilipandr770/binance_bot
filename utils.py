import sqlite3
import os

# Створюємо директорію для збереження даних
def create_data_directory():
    if not os.path.exists('./data'):
        os.makedirs('./data')

# Підключення до бази даних
def create_connection():
    create_data_directory()
    conn = sqlite3.connect('./data/crypto_data.db')
    return conn

# Створення таблиць для зберігання ордерів
def create_tables(conn):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS btc_usdt (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            price REAL,
            volume REAL,
            timestamp TEXT
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            direction TEXT,
            price REAL,
            stop_loss REAL,
            take_profit REAL
        )
    ''')
    conn.commit()

# Функція для запису ордерів
def record_order(direction, price, stop_loss, take_profit):
    conn = create_connection()
    create_tables(conn)
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO orders (timestamp, direction, price, stop_loss, take_profit) 
                      VALUES (datetime('now'), ?, ?, ?, ?)''', 
                   (direction, price, stop_loss, take_profit))
    conn.commit()
    conn.close()
