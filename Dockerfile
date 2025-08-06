# Use official Python slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project source code
COPY . /app/

# Expose port 8000 (Django + Daphne)
EXPOSE 8000

# Run migrations then start Daphne server (ASGI)
CMD ["sh", "-c", "daphne -b 0.0.0.0 -p 8000 BallotBlaze_Server.asgi:application"]
