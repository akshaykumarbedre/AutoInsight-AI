# AutoInsight AI FastAPI Dockerfile
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p tmp plots

# Expose port
EXPOSE 5001

# Set environment variables
ENV PORT=5001
ENV PYTHONPATH=/app
ENV WORKERS=1

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5001/health || exit 1

# Start the FastAPI server
CMD ["python", "-m", "uvicorn", "app_fastapi:app", "--host", "0.0.0.0", "--port", "5001", "--workers", "1"]
