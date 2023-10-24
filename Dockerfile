FROM python:3.11.6-alpine

WORKDIR /app

COPY . .

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add --no-cache mariadb-dev

RUN pip install -r requirements.txt

RUN apk del build-deps

