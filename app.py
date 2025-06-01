from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
import time
import os

app = Flask(__name__)

@app.route('/scraped-data')
def get_leadership():
    try:
        # Configure Selenium to use the correct endpoint
        selenium_url = "http://selenium:4444/wd/hub"  # Changed from localhost
        
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        driver = webdriver.Remote(
            command_executor=selenium_url,
            options=options
        )
        
        driver.get("https://www.triconinfotech.com/about/")
        time.sleep(8)  # Increased wait time
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        leadership = []
        
        for item in soup.select('.about-us-team__item'):
            leadership.append({
                'name': item.select_one('h3').get_text(strip=True) if item.select_one('h3') else None,
                'designation': item.select_one('p').get_text(strip=True) if item.select_one('p') else None,
                'linkedin': item.select_one('a[href*="linkedin.com"]')['href'] if item.select_one('a[href*="linkedin.com"]') else None
            })
            
        driver.quit()
        return jsonify(leadership)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))