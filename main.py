import logging
import os
from datetime import datetime

from config import PLATO_LOG_FILE_EXTENSION, PLATO_LOG_FILE_NAME, PLATO_MONGO_URL, PLATO_MONGO_COLLECTIONS
from helpers.plato_helper import find_all_entries_with_url
from handlers.main import on_entries_require_update, on_entries_up_to_date, on_dbpedia_types_require_update
from classes.MongoConnector import MongoConnector

logger = logging.getLogger(__name__)


def main():
    os.makedirs(os.path.dirname(f"{PLATO_LOG_FILE_NAME}.{PLATO_LOG_FILE_EXTENSION}"), exist_ok=True)
    logging.basicConfig(
        filename=f"{PLATO_LOG_FILE_NAME}_{datetime.now().strftime('%Y-%m-%d-%H:%M')}.{PLATO_LOG_FILE_EXTENSION}",
        filemode="w", format="[%(levelname)s] [%(asctime)s] [%(name)s] %(message)s", level=logging.DEBUG)
    logger.info("Logging started")

    mongo_connector = MongoConnector(PLATO_MONGO_URL)

    entry_links = find_all_entries_with_url()

    number_of_entries_in_db = mongo_connector.collections[PLATO_MONGO_COLLECTIONS["ENTRIES"]].count_documents({})

    # TODO: create update entries functionality
    if number_of_entries_in_db != len(entry_links):
        on_entries_require_update(mongo_connector, entry_links)

    on_entries_up_to_date()
    on_dbpedia_types_require_update(mongo_connector)

    logger.info("Logging finished")


if __name__ == "__main__":
    main()
