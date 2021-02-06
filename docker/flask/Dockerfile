FROM python:3.8
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /app
WORKDIR /app

# Copy files
COPY ./docker/flask/req.txt /app/req.txt
COPY ./docker/flask/start.sh /app/start.sh

# Copy folders
COPY ./src /app/src

# Install packages
RUN pip install -r /app/req.txt

# Run flask app
EXPOSE 8000

ENV FLASK_APP="src/main.py" FLASK_DEBUG=1 FLASK_ENV=docker

RUN ls -la /app && sed -i 's/\r//' /app/start.sh && chmod +x /app/start.sh

ENTRYPOINT ["./start.sh"]