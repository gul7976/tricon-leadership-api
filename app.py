from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

app = Flask(__name__)

@app.route('/scraped-data')
def scraped_data():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.get("https://www.triconinfotech.com/about/")
    time.sleep(5)  # wait for JS to load

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

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
