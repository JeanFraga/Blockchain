# FROM python:3.7.6-buster
FROM python:latest

RUN apt-get update 

ENV INSTALL_PATH /flask
RUN mkdir $INSTALL_PATH
WORKDIR $INSTALL_PATH

ENV PYTHONUNBUFFERED 1

RUN python3 -m pip install Flask gunicorn

COPY . .

CMD gunicorn -c "python:config.gunicorn" "BLOCKCHAIN:APP"