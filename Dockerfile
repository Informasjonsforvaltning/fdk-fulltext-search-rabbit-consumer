FROM python:3.11

COPY . /app
WORKDIR /app
RUN pip install --no-cache-dir poetry=="1.5.1"
RUN poetry install

CMD ["poetry", "run", "python", "-u", "src/main.py"]
