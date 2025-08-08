# AETHER Docker Image
# © 2024 AlgoRythm Tech - Built by Sri Aasrith Souri Kompella

FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Create necessary directories
RUN mkdir -p model_cache logs data

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV AETHER_ENV=production
ENV API_HOST=0.0.0.0
ENV API_PORT=8000
ENV WEB_PORT=8501

# Expose ports
EXPOSE 8000 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run AETHER
CMD ["python", "run.py", "--mode", "full", "--no-browser"]
