import time
import traceback
import sys

from pika.adapters.utils.connection_workflow import AMQPConnectorSocketConnectError
from pika.exceptions import AMQPChannelError, AMQPError, AMQPConnectionError

from adapter import rabbit
from config import LOG_LEVEL
from config import StackdriverJsonFormatter

import logging


if __name__ == '__main__':
    # logging.basicConfig(level=str(LOG_LEVEL.get('LEVEL')))
    logger = logging.getLogger()

    logHandler = logging.StreamHandler(sys.stdout)
    logHandler.setFormatter(StackdriverJsonFormatter())
    logger.addHandler(logHandler)
    listener = rabbit.Listener()

    while True:
        retry_sleep = 10
        try:
            listener.connect()
            listener.consume()

        # Do not recover on channel errors
        except AMQPChannelError as err:
            logging.error(f"{traceback.format_exc()} RabbitMQ channel error {err['message']}.")
            break
        # Recover on all other connection errors
        except (AMQPError, AMQPConnectorSocketConnectError, AMQPConnectionError) as err:
            logging.error(
                f"{traceback.format_exc()}RabbitMQ connection error "
                f"{err['message']}. Retrying in {retry_sleep} seconds ...")
            time.sleep(retry_sleep)
            continue
        # Log unknown exception and exit
        except Exception as err:
            logging.error(f"{traceback.format_exc()} Unknown exception: {err['message']}")
            break

    logging.info("Exiting ...")
