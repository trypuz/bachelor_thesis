import logging
import os
from datetime import datetime

from config import PLATO_LOG_FILE_EXTENSION, PLATO_LOG_FILE_NAME, PLATO_MONGO_URL, PLATO_MONGO_COLLECTIONS
from helpers.plato_helper import find_all_entries_with_url
from handlers.main import on_entries_require_update, on_entries_up_to_date, on_overall_stats_require_update
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

    on_overall_stats_require_update(mongo_connector)

    number_of_entries_in_db = mongo_connector.collections[PLATO_MONGO_COLLECTIONS["ENTRIES"]].count_documents({})

    # example1 = NLP("This entry is exclusively concerned with abduction in the modern sense, although there is a supplement on abduction in the historical sense, which had its origin in the work of Charles Sanders Peirce")
    # print(example1.get_ner_info())
    #
    # example2 = NLP("However, in the historically first sense, it refers to the place of explanatory reasoning in generating hypotheses, while in the sense in which it is used most frequently in the modern literature it refers to the place of explanatory reasoning in justifying hypotheses. In the latter sense, abduction is also often called “Inference to the Best Explanation.”")
    # print(example2.get_ner_info())
    #
    # example3 = NLP("However, in the historically first sense, it refers to the place of explanatory reasoning in generating hypotheses, while in the sense in which it is used most frequently in the modern literature it refers to the place of explanatory reasoning in justifying hypotheses. In the latter sense, abduction is also often called “Inference to the Best Explanation.”. Most philosophers agree that abduction (in the sense of “Inference to the Best Explanation“) is a type of inference that is frequently employed, in some form or other, both in everyday and in scientific reasoning.")
    # print(example3.get_ner_info())

    if number_of_entries_in_db != len(entry_links):
        on_entries_require_update(mongo_connector, entry_links)

    on_entries_up_to_date()

    logger.info("Logging finished")


if __name__ == "__main__":
    main()
