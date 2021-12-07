import logging
from json.decoder import JSONDecodeError
import traceback

import asyncio
import pika

from config import RABBITMQ
from .fulltext_ingest import ingest_for_index


class Listener:
    TYPE = 'topic'
    EXCHANGE = 'harvests'
    ROUTING_KEY = '*.reasoned'

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
        routing_key = method.routing_key
        try:
            logging.info(f"FROM: {routing_key}\nBody={body}")
            loop = asyncio.get_event_loop()
            loop.run_until_complete(ingest_for_index(routing_key.split('.')[0]))
        except KeyError:
            logging.error(
                f"{traceback.format_exc()} RabbitMQ: Received invalid operation type:  {routing_key['message']}"
            )
        except JSONDecodeError:
            logging.error(
                f"{traceback.format_exc()}RabbitMQ: Received invalid JSON:\n {body['message']}"
            )
