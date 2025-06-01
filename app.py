from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/quotes', methods=['GET'])
def get_quotes():
    url = "http://quotes.toscrape.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    quotes_list = []

    for quote_div in soup.select('div.quote'):
        text = quote_div.select_one('span.text').text.strip()
        author = quote_div.select_one('small.author').text.strip()
        quotes_list.append({
            "quote": text,
            "author": author
        })

    return jsonify(quotes_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
