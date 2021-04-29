import logging

from helpers.plato_helper import create_overall_ner_type_stats, create_all_ner_results, create_all_entry_models, \
    create_overall_ner_count_stats, create_overall_words_count_stats, create_overall_ner_coverage_stats, \
    create_overall_ner_occurrences_stats

logger = logging.getLogger(__name__)


def on_overall_stats_require_update(mongo_connector):
    logger.info("Starting update overall stats")
    create_overall_ner_type_stats(mongo_connector)
    create_overall_ner_count_stats(mongo_connector)
    create_overall_words_count_stats(mongo_connector)
    create_overall_ner_coverage_stats(mongo_connector)
    create_overall_ner_occurrences_stats(mongo_connector)
    logger.info("Overall stats updated")


def on_ner_results_require_update(mongo_connector):
    logger.info("Starting update NER results for entries")
    create_all_ner_results(mongo_connector)
    logger.info("NER results for entries extracted")
    on_overall_stats_require_update(mongo_connector)


def on_entries_require_update(mongo_connector, entry_links):
    logger.info("Entries require an update")
    create_all_entry_models(mongo_connector, entry_links)
    logger.info("Entries updated, next NER results should be updated")
    on_ner_results_require_update(mongo_connector)


def on_entries_up_to_date():
    logger.info("Entries and NER results are up to date")
