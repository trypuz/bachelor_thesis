import operator
import logging

from config import PLATO_NER_ALLOWED_TYPES

logger = logging.getLogger(__name__)


class NerResultsModel:
    def __init__(self, entry_id, ner_for_preamble, ner_for_main_text):
        self.entry_id = entry_id
        self.ner_results = {}
        self.ner_stats = {}

        self.add_ner_results(ner_for_preamble, ner_for_main_text)
        self.add_ner_stats()

    def add_ner_results(self, ner_for_preamble, ner_for_main_text):
        logger.debug("Filter NER results by allowed types")
        filtered_by_allowed_types_ner_for_preamble = [ner_entity for ner_entity in ner_for_preamble if
                                     (ner_entity["label"] in PLATO_NER_ALLOWED_TYPES)]
        filtered_by_allowed_types_ner_for_main_text = [ner_entity for ner_entity in ner_for_main_text if
                                      (ner_entity["label"] in PLATO_NER_ALLOWED_TYPES)]
        logger.debug("NER results filtered by allowed type")

        logger.debug("Preventing from double NER entries")
        checker_double_ner_texts_for_preamble = []
        checker_double_ner_texts_for_main_text = []

        filtered_by_allowed_types_and_double_texts_ner_for_preamble = []
        filtered_by_allowed_types_and_double_texts_ner_for_main_text = []

        for ner_entity_index, ner_entity in enumerate(filtered_by_allowed_types_ner_for_preamble):
            ner_checker = f"{ner_entity['text']}:{ner_entity['label']}"

            if ner_checker in checker_double_ner_texts_for_preamble:
                continue
            else:
                filtered_by_allowed_types_and_double_texts_ner_for_preamble.append(ner_entity)
                checker_double_ner_texts_for_preamble.append(ner_checker)

        for ner_entity_index, ner_entity in enumerate(filtered_by_allowed_types_ner_for_main_text):
            ner_checker = f"{ner_entity['text']}:{ner_entity['label']}"

            if ner_checker in checker_double_ner_texts_for_main_text:
                continue
            else:
                filtered_by_allowed_types_and_double_texts_ner_for_main_text.append(ner_entity)
                checker_double_ner_texts_for_main_text.append(ner_checker)

        logger.debug("NER results filtered by allowed types and prevented from double entries")

        self.ner_results = {
            "preamble": filtered_by_allowed_types_and_double_texts_ner_for_preamble,
            "main_text": filtered_by_allowed_types_and_double_texts_ner_for_main_text
        }

    def add_ner_stats(self):
        logger.debug("Starting calculate NER stats for single entry")
        ner_stats_for_preamble = {}
        ner_stats_for_main_text = {}

        for ner_type in PLATO_NER_ALLOWED_TYPES:
            ner_stats_for_preamble[ner_type] = 0
            ner_stats_for_main_text[ner_type] = 0

        for ner_entity in self.ner_results["preamble"]:
            ner_stats_for_preamble[ner_entity["label"]] += 1

        for ner_entity in self.ner_results["main_text"]:
            ner_stats_for_main_text[ner_entity["label"]] += 1

        self.ner_stats = {
            "preamble": dict(sorted(ner_stats_for_preamble.items(), key=operator.itemgetter(1), reverse=True)),
            "main_text": dict(sorted(ner_stats_for_main_text.items(), key=operator.itemgetter(1), reverse=True))
        }

        logger.debug("NER stats for single entry calculated")
