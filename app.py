from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import logging
import time
import os

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/api/leadership', methods=['GET'])
def get_leadership():
    try:
        # Set Chrome options for headless operation
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.add_argument("--window-size=1920x1080")

        # IMPORTANT: Provide the path to chromedriver if not in PATH
        # Example: driver_path = "/usr/local/bin/chromedriver"
        driver_path = os.environ.get("CHROMEDRIVER_PATH", "chromedriver")

        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)

        url = "https://www.triconinfotech.com/about/"
        logging.info(f"Accessing {url}")
        driver.get(url)

        # Wait for the team section to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "av-masonry-container"))
        )
        time.sleep(2)  # Extra wait for animations

        # Parse the page with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.quit()

        leaders = []
        team_section = soup.find("div", class_="av-masonry-container")

        if not team_section:
            logging.error("Leadership section not found.")
            return jsonify({"error": "Could not locate leadership section"}), 404

        members = team_section.find_all("div", class_="av-masonry-entry")

        for member in members:
            name_tag = member.find("h3", class_="av-masonry-entry-title")
            role_tag = member.find("div", class_="av-inner-masonry-content")
            link_tag = member.find("a", href=True)

            name = name_tag.get_text(strip=True) if name_tag else None
            role = role_tag.get_text(strip=True) if role_tag else None
            linkedin = link_tag["href"] if link_tag and "linkedin.com" in link_tag["href"] else None

            if name:
                leaders.append({
                    "name": name,
                    "designation": role,
                    "linkedin": linkedin
                })

        return jsonify({"executive_leadership": leaders})

    except Exception as e:
        logging.exception("An error occurred during scraping.")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
