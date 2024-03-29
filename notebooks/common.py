import yfinance as yf
import requests
import html

uri: str = ''
key: str = ''
email_URI: str = ''


def get_stock_price(symbol: str) -> float:
    stock = yf.Ticker(symbol)
    price = stock.history(period="1mo")['Close'].iloc[-1]
    return price


def send_logic_apps_email(to: str, content: str):
    try:
        json_payload = {'to': to, 'content': html.unescape(content)}
        headers = {'Content-Type': 'application/json'}
        response = requests.post(email_URI, json=json_payload, headers=headers)
        if response.status_code == 202:
            print("Email sent to: " + json_payload['to'])
    except:
        print("Unable to send the email via Logic Apps.")


def post_request(uri: str, key: str, payload: dict):
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
    json = post_request(uri, key, payload)
    return json["choices"][0]["message"]["content"]
