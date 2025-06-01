# Use official Selenium Chrome image
FROM selenium/standalone-chrome:latest

# Install Python and dependencies
USER root
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Expose port
EXPOSE 5000

# Run Flask directly (no gunicorn needed)
CMD ["python3", "app.py"]