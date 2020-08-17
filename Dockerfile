FROM python:3

COPY . /app
WORKDIR /app
RUN pip install pipenv
RUN pipenv install

RUN pipenv run python -u src/main.py
