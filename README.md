# fdk-fulltext-rabbit

The fdk-fulltext-rabbit is a stand-alone RabbitMQ consumer for fdk-fulltext-search

## Test the consumer locally

### Requirements

- poetry

### In your command line

```
% poetry install
% poetry run python src/main.py
```

## Test the consumer in docker

### Requirements

- docker

### In you command line

```
% docker build . -t eu.gcr.io/fdk-infra/fdk-fulltext-rabbit:latest
% docker run eu.gcr.io/fdk-infra/fdk-fulltext-rabbit:latest
```

## Test the consumer in docker-compose

### Requirements

- docker
- docker-compose

### In your command line

```
% docker-compose up  --build
```
