# Binance API ключі
API_KEY = "your_binance_api_key"  # Твій API ключ Binance
API_SECRET = "your_binance_secret_key"  # Твій секретний ключ Binance

# Параметри для торгівлі
AVAILABLE_USDT = 1000  # Доступний баланс в USDT
ORDER_AMOUNT = 15  # Початковий розмір ордера в USDT
INCREASED_ORDER_AMOUNT = 25  # Збільшений розмір ордера після перетину MA7 і MA25
PAIR = "BTCUSDT"  # Торгова пара

# Шлях до бази даних
DATABASE = './data/crypto_data.db'  # Шлях до вашої бази даних
STOP_LOSS_PERCENT = 1  # Стоп-лосс -1%
TAKE_PROFIT_PERCENT = 3  # Тейк-профіт +3%
