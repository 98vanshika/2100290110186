from flask import Flask, jsonify
import requests
from collections import deque

app = Flask(__name__)

WINDOW_SIZE = 10
NUMBER_STORE = {
    'p': deque(maxlen=WINDOW_SIZE),
    'f': deque(maxlen=WINDOW_SIZE),
    'e': deque(maxlen=WINDOW_SIZE),
    'r': deque(maxlen=WINDOW_SIZE)
}

THIRD_PARTY_API = {
    'p': 'http://20.244.56.144/test/primes',
    'f': 'http://20.244.56.144/test/fibo',
    'e': 'http://20.244.56.144/test/even',
    'r': 'http://20.244.56.144/test/rand'
}

def fetch_numbers(number_type):
    try:
        response = requests.get(THIRD_PARTY_API[number_type], timeout=0.5)
        if response.status_code == 200:
            return response.json().get('numbers', [])
    except requests.exceptions.RequestException:
        return []

@app.route('/numbers/<number_type>', methods=['GET'])
def get_number(number_type):
    if number_type not in NUMBER_STORE:
        return jsonify({"error": "Invalid number type"}), 400

    new_numbers = fetch_numbers(number_type)
    before_store = list(NUMBER_STORE[number_type])
    
    for number in new_numbers:
        if number not in NUMBER_STORE[number_type]:
            NUMBER_STORE[number_type].append(number)
    
    after_store = list(NUMBER_STORE[number_type])
    avg = sum(after_store) / len(after_store) if after_store else 0
    
    response = {
        "windowPrevState": before_store,
        "windowCurrState": after_store,
        "numbers": new_numbers,
        "avg": round(avg, 2)
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(port=9876, debug=True)
