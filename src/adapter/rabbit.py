import logging
from json.decoder import JSONDecodeError

import pika
import requests

from config import RABBITMQ, FULLTEXT_SEARCH


class Listener:
    TYPE = 'topic'
    EXCHANGE = 'harvests'
    ROUTING_KEY = '*.harvester.UpdateSearchTrigger'

    def __init__(self):
        self._channel = None
        self._conn = None
        self._credentials = pika.PlainCredentials(username=RABBITMQ.get('USERNAME'),
                                                  password=RABBITMQ.get('PASSWORD'))
        self._host = RABBITMQ.get('HOST')

    def connect(self):
        if not self._conn or self._conn.is_closed:
            logging.info("Establishing RabbitMQ connection ...")
            self._conn = pika.BlockingConnection(
                pika.ConnectionParameters(host=self._host, credentials=self._credentials)
            )
        else:
            logging.info("RabbitMQ connection has already been established")

        self._channel = self._conn.channel()
        self._channel.exchange_declare(exchange=self.EXCHANGE, exchange_type=self.TYPE)

        logging.info(f"RabbitMQ successfully connected to {self._host}")

    def consume(self):
        declaration = self._channel.queue_declare('', exclusive=True, auto_delete=True)
        queue_name = declaration.method.queue

        logging.info(f"RabbitMQ queue declared: {queue_name}")

        self._channel.queue_bind(
            exchange=self.EXCHANGE, queue=queue_name, routing_key=self.ROUTING_KEY
        )
        self._channel.basic_consume(
            queue=queue_name, auto_ack=True, on_message_callback=self.on_receive
        )

        logging.info(f"RabbitMQ consumer starting (TYPE={self.TYPE}, EXCHANGE={self.EXCHANGE} "
                     f"KEY={self.ROUTING_KEY}) ...")

        return self._channel.start_consuming()

    @staticmethod
    def on_receive(ch, method, properties, body):
        fulltext_endpoint = f"{FULLTEXT_SEARCH.get('BASE_URL')}/indices"

        routing_key = method.routing_key
        logging.info(f"FROM: {routing_key}\nBody={body}")
        try:
            index = routing_key.split('.')[0]
            logging.info(f"RabbitMQ ingesting index \"{index}\" "
                         f"into fulltext search: {fulltext_endpoint}")
            try:
                response = requests.post(
                    url=fulltext_endpoint,
                    params={'name': index},
                    headers={'X-API-KEY': FULLTEXT_SEARCH.get('API_KEY')}
                )
                response.raise_for_status()
                logging.info(f"Successfully ingested {index}")

            except requests.HTTPError as e:
                logging.error(f"FDK Fulltext Search HTTP error: {e}")

        except KeyError:
            logging.error(f"RabbitMQ: Received invalid operation type: {routing_key}")
        except JSONDecodeError:
            logging.error(f"RabbitMQ: Received invalid JSON:\n {body}")
