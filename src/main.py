import logging
import time
import traceback

from pika.adapters.utils.connection_workflow import AMQPConnectorSocketConnectError
from pika.exceptions import AMQPChannelError, AMQPError, AMQPConnectionError

from adapter import rabbit
from config import LOGGING

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
            logging.error(f"RabbitMQ channel error {traceback.format_exc()} {err['message']}.")
            break
        # Recover on all other connection errors
        except (AMQPError, AMQPConnectorSocketConnectError, AMQPConnectionError) as err:
            logging.error(
                f"RabbitMQ connection error {traceback.format_exc()} "
                f"{err['message']}. Retrying in {retry_sleep} seconds ...")
            time.sleep(retry_sleep)
            continue
        # Log unknown exception and exit
        except Exception as err:
            logging.error(f"Unknown exception: {traceback.format_exc()} {err['message']}")
            break

    logging.info("Exiting ...")
