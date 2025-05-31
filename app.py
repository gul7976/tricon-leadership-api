from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/scraped-data')
def scraped_data():
    url = "https://www.triconinfotech.com/about/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    leadership = []
    team_divs = soup.select('div.about-us-team__item')

    for div in team_divs:
        name = div.select_one('h3')
        title = div.select_one('p')
        linkedin = div.select_one('a[href*="linkedin.com"]')

        leadership.append({
            "name": name.get_text(strip=True) if name else None,
            "designation": title.get_text(strip=True) if title else None,
            "linkedin_url": linkedin['href'] if linkedin else None
        })

    return jsonify(leadership)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
