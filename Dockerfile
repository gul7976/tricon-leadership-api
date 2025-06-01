# Use official Selenium Chrome image as base
FROM selenium/standalone-chrome:latest

# Install Python and pip
USER root
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose Flask port
EXPOSE 5000

# Command to run Flask app
CMD ["python3", "app.py"]