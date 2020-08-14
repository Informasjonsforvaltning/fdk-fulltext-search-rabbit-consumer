import logging
import time

from pika.adapters.utils.connection_workflow import AMQPConnectorSocketConnectError
from pika.exceptions import AMQPChannelError, AMQPError, AMQPConnectionError

from src.adapter import rabbit
from src.config import LOGGING

if __name__ == '__main__':
    logging.basicConfig(level=LOGGING.get('LEVEL'))
    listener = rabbit.Listener()

    while True:
        retry_sleep = 10
        try:
            listener.connect()
            listener.consume()

        # Do not recover on channel errors
        except AMQPChannelError as err:
            logging.error(f"RabbitMQ channel error {err}.")
            break
        # Recover on all other connection errors
        except (AMQPError, AMQPConnectorSocketConnectError, AMQPConnectionError) as err:
            logging.error(f"RabbitMQ connection error {err}. Retrying in {retry_sleep} seconds ...")
            time.sleep(retry_sleep)
            continue
        # Log unknown exception and exit
        except Exception as err:
            logging.error(f"Unknown exception: {err}")
            break

    logging.info("Exiting ...")
