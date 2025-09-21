# Use official Python image
FROM python:3.11-slim

# Prevents Python from writing .pyc files and buffering output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system deps if needed (gcc for some packages)
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
RUN mkdir common keeper
COPY common/requirements.txt ./common
COPY keeper/requirements.txt ./keeper

# Install Python dependencies
RUN pip install --no-cache-dir -r common/requirements.txt
RUN pip install --no-cache-dir -r keeper/requirements.txt

COPY ./keeper ./keeper
COPY ./common ./common

# Expose port (optional metadata)
EXPOSE 8000

# Run Uvicorn — production ready
CMD ["uvicorn", "keeper.main:app", "--host", "0.0.0.0", "--port", "8000"]