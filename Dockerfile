# Use the official Python image from the Docker Hub
FROM python:3.9.17-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc git postgresql libpq-dev default-mysql-client libmariadb-dev-compat libmariadb-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . /app/

WORKDIR /app
ENV PATH="$PATH:/app/project/"

RUN django-admin collectstatic --no-input
RUN django-admin migrate --noinput

# Run the application
CMD ["gunicorn", "project.wsgi:application", "--bind", "0.0.0.0:$PORT"]
