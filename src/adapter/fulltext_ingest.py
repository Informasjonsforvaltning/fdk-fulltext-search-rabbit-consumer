import logging
import traceback

import requests

from config import FULLTEXT_SEARCH


async def ingest_for_index(index_key):
    try:
        fulltext_endpoint = f"{FULLTEXT_SEARCH.get('BASE_URL')}/indices"
        logging.info(f"RabbitMQ ingesting index \"{index_key}\" "
                     f"into fulltext search: {fulltext_endpoint}")
        response = requests.post(
            url=fulltext_endpoint,
            params={'name': index_key},
            headers={'X-API-KEY': FULLTEXT_SEARCH.get('API_KEY')},
            timeout=1800
        )
        response.raise_for_status()
        logging.info(f"Successfully ingested {index_key}")

    except requests.HTTPError:
        logging.error(f"{traceback.format_exc()} HTTP error when ingesting {index_key}")
    except Exception:
        logging.error(f"{traceback.format_exc()} Exception when ingesting {index_key}")
