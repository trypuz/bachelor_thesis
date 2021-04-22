import logging
from SPARQLWrapper import JSON

from config import PLATO_TOC_URL, PLATO_ROOT_URL, PLATO_STATS_IDS, PLATO_NER_TO_DBPEDIA_TYPES_MAP, \
    PLATO_SPARQL_QUERY_FOR_GETTING_TYPE_PROPS
from classes.EntryLinkModel import EntryLinkModel
from classes.EntryModel import EntryModel
from classes.MongoConnector import MongoConnector
from classes.StatsModel import StatsModel
from classes.NerResultsModel import NerResultsModel
from classes.DbpediaTypeModel import DbpediaTypeModel
from classes.NLP import NLP
from helpers.url_helper import get_source_from_url, convert_source_to_soup

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
    preamble = entry_soup_handler.find(id="preamble").get_text()
    main_text = entry_soup_handler.find(id="main-text").get_text()
    logger.debug(f"Info about <{entry_link.name}> retrieved")

    return EntryModel(entry_id=entry_id, title=title, preamble=preamble, main_text=main_text)


def create_all_entry_models(mongo_connector: MongoConnector, entry_links):
    for entry_id, entry_link in enumerate(entry_links):
        entry_soup_handler = get_entry_soup_handler(entry_link)
        entry_model = get_entry_model(entry_id, entry_soup_handler, entry_link)
        mongo_connector.add_entry_to_collection(entry_model)


def create_all_ner_results(mongo_connector: MongoConnector):
    entries_from_db = mongo_connector.get_all_entries_from_collection()
    entries_from_db = [document for document in entries_from_db]

    for entry in entries_from_db:
        nlp_for_preamble = NLP(entry["preamble"])
        nlp_for_main_text = NLP(entry["main_text"])
        ner_results_for_entry = NerResultsModel(entry["entry_id"], nlp_for_preamble.get_ner_info(),
                                                nlp_for_main_text.get_ner_info())
        mongo_connector.add_ner_results_for_single_entry_to_collection(ner_results_for_entry)


def create_overall_ner_stats(mongo_connector: MongoConnector):
    ner_results_from_db = mongo_connector.get_all_ner_results_from_collection()
    ner_results_from_db = [document for document in ner_results_from_db]

    overall_ner_stats_model = StatsModel(stats_id=PLATO_STATS_IDS["OVERALL_NER_STATS"],
                                         stats=StatsModel.calculate_overall_ner_stats(ner_results_from_db))

    mongo_connector.add_stats_to_collection(overall_ner_stats_model)


def create_dbpedia_types(mongo_connector: MongoConnector, sparql_wrapper):
    for ner_to_dbpedia_type_key, ner_to_dbpedia_type_value in PLATO_NER_TO_DBPEDIA_TYPES_MAP.items():
        if ner_to_dbpedia_type_value == "":
            continue

        sparql_wrapper.setQuery(PLATO_SPARQL_QUERY_FOR_GETTING_TYPE_PROPS.format(ner_to_dbpedia_type_value))
        sparql_wrapper.setReturnFormat(JSON)
        results = sparql_wrapper.query().convert()

        ner_type = ner_to_dbpedia_type_key
        dbpedia_type_name = ner_to_dbpedia_type_value
        props = {}

        for result in results["results"]["bindings"]:
            prop_name_formatted = result["prop"]["value"].replace(".", ",")
            props[prop_name_formatted] = result["count"]["value"]

        dbpedia_type_model = DbpediaTypeModel(ner_type=ner_type, name=dbpedia_type_name, props=props)
        mongo_connector.add_dbpedia_type_to_collection(dbpedia_type_model)


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
