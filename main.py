import logging
import os
from SPARQLWrapper import SPARQLWrapper, JSON
from datetime import datetime

from config import PLATO_LOG_FILE_EXTENSION, PLATO_LOG_FILE_NAME, PLATO_MONGO_URL, PLATO_MONGO_COLLECTIONS, \
    PLATO_STATS_IDS, PLATO_DBPEDIA_URL
from helpers.plato_helper import find_all_entries_with_url
from handlers.main import on_entries_require_update, on_entries_up_to_date
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

    if number_of_entries_in_db != len(entry_links):
        on_entries_require_update(mongo_connector, entry_links)

    on_entries_up_to_date()

    overall_ner_occurrences_stats = mongo_connector.get_overall_stats_by_id(
        PLATO_STATS_IDS["OVERALL_NER_OCCURRENCES_STATS"])

    for key, value in overall_ner_occurrences_stats["value"].items():
        for idx, (key2, value2) in enumerate(value.items()):
            if idx == 1:
                break

            print("Key:", key2)
            sparql = SPARQLWrapper(PLATO_DBPEDIA_URL)
            sparql.setQuery(f"""
                select distinct ?entity ?label {{
?entity rdfs:label ?label .
filter langMatches(lang(?label),"en") 
filter contains(?label,"{key2.split('__')[0]}") 
}}
            """)
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()
            for result in results["results"]["bindings"]:
                print(result["entity"]["value"])

    logger.info("Logging finished")


if __name__ == "__main__":
    main()
