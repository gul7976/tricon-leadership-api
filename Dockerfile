# Use official Python slim image
FROM python:3.10-slim

# Install dependencies for Chrome and Selenium
RUN apt-get update && apt-get install -y \
    wget \
    gnupg2 \
    ca-certificates \
    fonts-liberation \
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libgdk-pixbuf2.0-0 \
    libnspr4 \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    xdg-utils \
    unzip \
    curl \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Add Google's official Linux signing key and Chrome repo
RUN wget -q -O /usr/share/keyrings/google-linux-signing-key.gpg https://dl.google.com/linux/linux_signing_key.pub && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-linux-signing-key.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y google-chrome-stable --fix-missing && \
    rm -rf /var/lib/apt/lists/*

# Get Chrome major version installed
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d '.' -f 1) && \
    echo "Chrome major version is $CHROME_VERSION" && \
    CHROMEDRIVER_VERSION=$(wget -qO- "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION") && \
    echo "ChromeDriver version is $CHROMEDRIVER_VERSION" && \
    wget -O /tmp/chromedriver.zip "https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip" && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    rm /tmp/chromedriver.zip && \
    chmod +x /usr/local/bin/chromedriver

# Set environment variables for Chrome/Chromedriver for Selenium
ENV PATH="/usr/local/bin/:${PATH}"
ENV CHROME_BIN="/usr/bin/google-chrome"
ENV CHROMEDRIVER_PATH="/usr/local/bin/chromedriver"

# Copy your app code into the container
COPY . /app
WORKDIR /app

# Install Python dependencies (make sure you have requirements.txt)
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for Flask app
EXPOSE 5000

# Command to run your Flask app
CMD ["python", "app.py"]
