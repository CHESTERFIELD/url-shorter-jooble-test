FROM python:3.8
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /app
WORKDIR /app

# Copy files
COPY ./docker/flask/req.txt /app/req.txt
COPY ./docker/flask/start.sh /app/start.sh

# Copy folders
COPY ./src /app/src

# install system dependencies
RUN apt-get update && apt-get install -y netcat

# Install packages
RUN pip install -r /app/req.txt

# Run flask app
EXPOSE 8000

RUN ls -la /app && sed -i 's/\r//' /app/start.sh && chmod +x /app/start.sh