import logging
from SPARQLWrapper import SPARQLWrapper

from config import PLATO_DBPEDIA_URL
from helpers.plato_helper import create_overall_ner_stats, create_all_ner_results, create_all_entry_models, \
    create_dbpedia_types

logger = logging.getLogger(__name__)


def on_dbpedia_types_require_update(mongo_connector):
    logger.info("Starting update DBPedia types")
    sparql_wrapper = SPARQLWrapper(PLATO_DBPEDIA_URL)
    create_dbpedia_types(mongo_connector, sparql_wrapper)
    logger.info("DBPedia types updated")


def on_overall_ner_stats_require_update(mongo_connector):
    logger.info("Starting update overall NER stats")
    create_overall_ner_stats(mongo_connector)
    logger.info("Overall NER stats updated")
    on_dbpedia_types_require_update()


def on_ner_results_require_update(mongo_connector):
    logger.info("Starting update NER results for entries")
    create_all_ner_results(mongo_connector)
    logger.info("NER results for entries extracted")
    on_overall_ner_stats_require_update(mongo_connector)


def on_entries_require_update(mongo_connector, entry_links):
    logger.info("Entries require an update")
    create_all_entry_models(mongo_connector, entry_links)
    logger.info("Entries updated, next NER results should be updated")
    on_ner_results_require_update(mongo_connector)


def on_entries_up_to_date():
    logger.info("Entries and NER results are up to date")
