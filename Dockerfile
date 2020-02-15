FROM python:3.7.6-slim-buster
RUN apt-get update && apt-get -y upgrade
RUN apt-get -y install festival festvox-ca-ona-hts lame

ENV PORT 8100

RUN mkdir -p /srv

COPY Pipfile /srv/
COPY *.py /srv/
COPY *.txt /srv/
COPY ./tests /srv/tests

WORKDIR /srv

RUN pip install pipenv
RUN pipenv install

EXPOSE $PORT
ENTRYPOINT pipenv run gunicorn tts-service:app -b 0.0.0.0:$PORT
