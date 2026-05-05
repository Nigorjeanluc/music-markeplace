FROM python:3.12-slim as builder

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code to /app/
COPY backend/ .

# Build frontend
COPY frontend/ ./frontend/
RUN cd frontend && npm install && npm run build

# Make startup script executable
RUN chmod +x /app/start.sh

# Expose port
EXPOSE 8000

# Run migrations, seed, and start server
CMD ["/app/start.sh"]
