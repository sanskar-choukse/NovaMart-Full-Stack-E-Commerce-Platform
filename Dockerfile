# Use Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput --settings=config.settings.prod || true

# Copy startup script
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Create media directory
RUN mkdir -p /app/media

# Expose port
EXPOSE 8000

# Run gunicorn
CMD ["/app/start.sh"]
