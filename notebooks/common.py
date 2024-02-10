import yfinance as yf
import requests
import html

uri: str = ''
key: str = ''


def get_stock_price(symbol: str) -> float:
    stock = yf.Ticker(symbol)
    price = stock.history(period="1d")['Close'].iloc[-1]
    return price


def send_logic_apps_email(email_URI: str, to: str, content: str):
    json_payload = {'to': to, 'content': html.unescape(content)}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(email_URI, json=json_payload, headers=headers)
    if response.status_code == 202:
        print("Email sent to: " + json_payload['to'])


def send_post(uri: str, key: str, payload: dict):
    headers = {'Content-Type': 'application/json',
               'api-key': key}
    response = requests.post(uri, json=payload, headers=headers)
    response.raise_for_status()
    if response.status_code == 200:
        return response.json()


def process_completion(prompt: str, max_tokens=100, temperature=0.3) -> str:
    payload = {
        "messages": [
            {
                "role": "assistant",
                "content": prompt
            }

        ],
        "max_tokens": max_tokens,
        "temperature": temperature
    }
    json = send_post(uri, key, payload)
    return json["choices"][0]["message"]["content"]
