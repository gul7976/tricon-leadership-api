from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

app = Flask(__name__)

@app.route('/scraped-data')
def scraped_data():
    try:
        # Configure Selenium to use the pre-installed Chrome
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        driver = webdriver.Remote(
            command_executor='http://localhost:4444/wd/hub',
            options=options
        )
        
        driver.get("https://www.triconinfotech.com/about/")
        time.sleep(5)  # Wait for JS to load
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        leadership = []
        
        # Extract data (adjust selectors as needed)
        for div in soup.select('div.about-us-team__item'):
            name = div.select_one('h3').get_text(strip=True) if div.select_one('h3') else None
            title = div.select_one('p').get_text(strip=True) if div.select_one('p') else None
            linkedin = div.select_one('a[href*="linkedin.com"]')
            
            leadership.append({
                "name": name,
                "designation": title,
                "linkedin_url": linkedin['href'] if linkedin else None
            })
        
        driver.quit()
        return jsonify(leadership)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)