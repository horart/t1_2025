# Use official Python runtime as base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY rater/requirements.txt ./rater/
COPY common/requirements.txt ./common/

# Install Python dependencies
RUN pip install --no-cache-dir -r rater/requirements.txt
RUN pip install --no-cache-dir -r common/requirements.txt

# Copy project code
COPY rater ./rater/
COPY common ./common/

# Optional: Create non-root user for security
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose port (if it's a web app)
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "rater.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
# CMD ["tail",  "-f", "/dev/null"]