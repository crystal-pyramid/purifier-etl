from binance.client import Client
import json,os


def to_json(element):
    return json.dumps(element)

# Binanceクライアントの初期化関数
def initialize_binance_client():
    with open(os.getenv('API_KEY_PATH')) as f:
        d = json.load(f)
        api_key = d.get("api_key")
        api_secret = d.get("secret_key")
    return Client(api_key, api_secret)

# ビットコイン価格を取得する関数
def get_btc_price(element, client):
    btc_price = client.get_symbol_ticker(symbol="BTCUSDT")
    return btc_price