FROM python:3

COPY . /app
WORKDIR /app
RUN pip install pipenv
RUN pipenv install

CMD ["pipenv", "run", "python", "-u", "src/main.py"]
