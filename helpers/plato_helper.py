import logging

from config import PLATO_TOC_URL, PLATO_ROOT_URL, PLATO_STATS_IDS
from classes.EntryLinkModel import EntryLinkModel
from classes.EntryModel import EntryModel
from classes.MongoConnector import MongoConnector
from classes.StatsModel import StatsModel
from classes.NerResultsModel import NerResultsModel
from classes.NLP import NLP
from helpers.url_helper import get_source_from_url, convert_source_to_soup
from helpers.string_helper import remove_extra_whitespaces

logger = logging.getLogger(__name__)


def get_toc_soup_handler():
    logger.debug("Getting TOC source started")
    html_source = get_source_from_url(PLATO_TOC_URL)
    logger.debug("TOC source retrieved")
    return convert_source_to_soup(html_source)


def get_entry_soup_handler(entry_link):
    logger.debug(f"Getting entry <{entry_link.name}> page source")
    html_source = get_source_from_url(f"{PLATO_ROOT_URL}/{entry_link.url}")
    logger.debug("Entry page source retrieved")
    return convert_source_to_soup(html_source)


def get_entry_model(entry_id, entry_soup_handler, entry_link):
    logger.debug(f"Retrieving info about entry <{entry_link.name}>")
    title = entry_soup_handler.h1.get_text()
    preamble = remove_extra_whitespaces(entry_soup_handler.find(id="preamble").get_text())
    main_text = remove_extra_whitespaces(entry_soup_handler.find(id="main-text").get_text())
    words_count = len(preamble.split()) + len(main_text.split())

    logger.debug(f"Info about <{entry_link.name}> retrieved")

    return EntryModel(entry_id=entry_id, title=title, preamble=preamble, main_text=main_text, words_count=words_count)


def create_all_entry_models(mongo_connector: MongoConnector, entry_links):
    for entry_id, entry_link in enumerate(entry_links):
        entry_soup_handler = get_entry_soup_handler(entry_link)
        entry_model = get_entry_model(entry_id, entry_soup_handler, entry_link)
        mongo_connector.add_entry_to_collection(entry_model)


def create_all_ner_results(mongo_connector: MongoConnector):
    entries_from_db = mongo_connector.get_all_entries_from_collection()
    entries_from_db = [document for document in entries_from_db]

    for entry in entries_from_db:
        text_for_nlp = NLP(entry["preamble"] + entry["main_text"])
        ner_results_for_entry = NerResultsModel(entry["entry_id"], text_for_nlp.get_ner_info(), entry["words_count"])
        mongo_connector.add_ner_results_for_single_entry_to_collection(ner_results_for_entry)


def generate_stats_model(stats_id, value):
    overall_stats_model = StatsModel(stats_id=stats_id,
                                     value=value)
    return overall_stats_model


def create_overall_ner_type_stats(mongo_connector: MongoConnector):
    ner_results_from_db = mongo_connector.get_all_ner_results_from_collection()
    ner_results_from_db = [document for document in ner_results_from_db]

    overall_ner_type_stats_func = StatsModel.calculate_overall_ner_type_stats(ner_results_from_db)
    overall_ner_type_stats_model = generate_stats_model(PLATO_STATS_IDS["OVERALL_NER_TYPE_STATS"],
                                                        overall_ner_type_stats_func)

    mongo_connector.add_stats_to_collection(overall_ner_type_stats_model)


def create_overall_ner_count_stats(mongo_connector: MongoConnector):
    ner_results_from_db = mongo_connector.get_all_ner_results_from_collection()
    ner_results_from_db = [document for document in ner_results_from_db]

    overall_ner_count_stats_func = StatsModel.calculate_overall_ner_count_stats(ner_results_from_db)
    overall_ner_count_stats_model = generate_stats_model(PLATO_STATS_IDS["OVERALL_NER_COUNT_STATS"],
                                                         overall_ner_count_stats_func)

    mongo_connector.add_stats_to_collection(overall_ner_count_stats_model)


def create_overall_words_count_stats(mongo_connector: MongoConnector):
    entries_results_from_db = mongo_connector.get_all_entries_from_collection()
    entries_results_from_db = [document for document in entries_results_from_db]

    overall_words_count_stats_func = StatsModel.calculate_overall_words_count_stats(entries_results_from_db)
    overall_words_count_stats_model = generate_stats_model(PLATO_STATS_IDS["OVERALL_WORDS_COUNT_STATS"],
                                                           overall_words_count_stats_func)

    mongo_connector.add_stats_to_collection(overall_words_count_stats_model)


def create_overall_ner_coverage_stats(mongo_connector: MongoConnector):
    overall_ner_count_stats = mongo_connector.get_overall_stats_by_id(PLATO_STATS_IDS["OVERALL_NER_COUNT_STATS"])
    overall_words_count_stats = mongo_connector.get_overall_stats_by_id(PLATO_STATS_IDS["OVERALL_WORDS_COUNT_STATS"])

    overall_ner_coverage_stats_func = StatsModel.calculate_overall_ner_coverage_stats(overall_ner_count_stats["value"],
                                                                                      overall_words_count_stats[
                                                                                          "value"])
    overall_ner_coverage_stats_model = generate_stats_model(PLATO_STATS_IDS["OVERALL_NER_COVERAGE_STATS"],
                                                            overall_ner_coverage_stats_func)

    mongo_connector.add_stats_to_collection(overall_ner_coverage_stats_model)


def create_overall_ner_occurrences_stats(mongo_connector: MongoConnector):
    ner_results_from_db = mongo_connector.get_all_ner_results_from_collection()
    ner_results_from_db = [document for document in ner_results_from_db]

    overall_ner_occurrences_stats_func = StatsModel.calculate_overall_ner_occurrences_stats(ner_results_from_db)
    overall_ner_occurrences_stats_model = generate_stats_model(PLATO_STATS_IDS["OVERALL_NER_OCCURRENCES_STATS"],
                                                               overall_ner_occurrences_stats_func)

    mongo_connector.add_stats_to_collection(overall_ner_occurrences_stats_model)


def find_all_entries_with_url():
    soup_handler = get_toc_soup_handler()

    logger.debug("Finding all entries from TOC with theirs URL started")
    entries = []

    content = soup_handler.find(id="content")

    for entry in content.find_all("li"):
        if entry.a:
            entry_a_element = entry.a
            if entry_a_element.has_attr("href") and entry_a_element["href"] != "#":
                if entry_a_element["href"] not in [entry_checker.url for entry_checker in entries]:
                    entries.append(EntryLinkModel(entry_a_element.get_text(), entry_a_element['href']))

    logger.debug("Entries from TOC retrieved")

    return entries
