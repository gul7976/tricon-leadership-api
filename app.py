from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/scraped-data')
def scraped_data():
    url = "https://www.triconinfotech.com/about/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    leadership = []

    # Inspecting the site shows leaders are in divs with class "about-us-team"
    team_divs = soup.select('div.about-us-team div.about-us-team__item')

    for div in team_divs:
        name = div.select_one('h3').get_text(strip=True) if div.select_one('h3') else None
        designation = div.select_one('p').get_text(strip=True) if div.select_one('p') else None
        linkedin_tag = div.select_one('a[href*="linkedin.com"]')
        linkedin_url = linkedin_tag['href'] if linkedin_tag else None

        leadership.append({
            'name': name,
            'designation': designation,
            'linkedin_url': linkedin_url
        })

    return jsonify(leadership)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
