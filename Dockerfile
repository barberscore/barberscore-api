# Use the official Python image from the Docker Hub

# FROM balenalib/tdpzu9-ubuntu-python:3.9-build
FROM ubuntu:20.04
RUN echo 'Building Ubuntu'

ARG DEBIAN_FRONTEND=noninteractive
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl wget python3.9 python3-dev python3-pip gcc git postgresql libpq-dev libmariadb-dev-compat libmariadb-dev libjpeg-dev xfonts-75dpi xfonts-base libfontconfig1-dev libx11-6 libxcb1 libxext6 libxrender1 xz-utils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.4/wkhtmltox-0.12.4_linux-generic-amd64.tar.xz
RUN ls
RUN tar xvJf wkhtmltox-0.12.4_linux-generic-amd64.tar.xz
RUN cp wkhtmltox/bin/wkhtmlto* /usr/bin/
# RUN wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.5/wkhtmltox_0.12.5-1.bionic_amd64.deb
# RUN dpkg -i wkhtmltox_0.12.5-1.bionic_amd64.deb
# RUN apt-get install -y -f
# RUN ln -s /usr/local/bin/wkhtmltopdf /usr/bin/wkhtmltopdf


# RUN ln -s /usr/lib/aarch64-linux-gnu/libjpeg.so.62 /usr/lib/aarch64-linux-gnu/libjpeg.so.8
RUN rm -f /usr/bin/python3 && ln -s /usr/bin/python3.9 /usr/bin/python3

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . /app/

WORKDIR /app
ENV PATH="$PATH:/app/project/"

# RUN python manage.py collectstatic --no-input
# RUN python manage.py migrate --noinput
CMD python3

# Run the application
# CMD gunicorn project.wsgi:application  --bind 0.0.0.0:$PORT
