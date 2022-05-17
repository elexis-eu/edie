FROM python:3.8-slim

WORKDIR /app
COPY . /app

RUN apt-get update
RUN apt-get upgrade -y

RUN pip install -r requirements.txt

WORKDIR /app/src

ENTRYPOINT ["sh", "-c", "gunicorn -w 4 \"rest:create_app()\" --bind 0.0.0.0:5000"]
