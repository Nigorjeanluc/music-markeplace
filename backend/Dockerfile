FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Copy and use startup script
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Run migrations, seed, and start server (handled by start.sh)
CMD ["/app/start.sh"]
