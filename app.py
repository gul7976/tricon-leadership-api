from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
import time

app = Flask(__name__)

@app.route('/scraped-data')
def scraped_data():
    try:
        # Connect to Selenium Hub (running in same container)
        driver = webdriver.Remote(
            command_executor='http://localhost:4444/wd/hub',
            options=webdriver.ChromeOptions()
        )
        
        driver.get("https://www.triconinfotech.com/about/")
        time.sleep(5)
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        leadership = []
        
        # Adjust these selectors based on actual page structure
        for member in soup.select('.about-us-team__item'):
            leadership.append({
                "name": member.select_one('h3').get_text(strip=True) if member.select_one('h3') else None,
                "designation": member.select_one('p').get_text(strip=True) if member.select_one('p') else None,
                "linkedin": member.select_one('a[href*="linkedin.com"]')['href'] if member.select_one('a[href*="linkedin.com"]') else None
            })
            
        driver.quit()
        return jsonify(leadership)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)