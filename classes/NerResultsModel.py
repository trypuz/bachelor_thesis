import operator
import logging

from config import PLATO_NER_ALLOWED_TYPES

logger = logging.getLogger(__name__)


class NerResultsModel:
    def __init__(self, entry_id, text_with_ner_extracted, chars_count):
        self.entry_id = entry_id
        self.chars_count = chars_count
        self.ner_results = {}
        self.ner_stats = {}

        self.add_ner_results(text_with_ner_extracted)
        self.add_ner_stats()

    def add_ner_results(self, text_for_ner_extraction):
        logger.debug("Filter NER results by allowed types")
        filtered_by_allowed_types_ner = [ner_entity for ner_entity in text_for_ner_extraction if
                                         (ner_entity["label"] in PLATO_NER_ALLOWED_TYPES)]
        logger.debug("NER results filtered by allowed type")

        self.ner_results = filtered_by_allowed_types_ner

    def add_ner_stats(self):
        logger.debug("Starting calculate NER stats for single entry")
        ner_count = 0
        ner_type_stats = {}
        ner_occurrences = {}

        for ner_type in PLATO_NER_ALLOWED_TYPES:
            ner_type_stats[ner_type] = 0

        for ner_entity in self.ner_results:
            for ner_entity_text_word in ner_entity["text"].split():
                ner_count += len(ner_entity_text_word)

            modified_ner_entity_text = ner_entity["text"].replace('.', '_').replace('$', 'DOLLAR-')
            ner_occurrences_key_name = f"{modified_ner_entity_text}__{ner_entity['label']}"
            ner_occurrences[ner_occurrences_key_name] = (ner_occurrences[ner_occurrences_key_name] + 1) if (
                        ner_occurrences_key_name in ner_occurrences) else 1
            ner_type_stats[ner_entity["label"]] += 1

        ner_type_stats = dict(sorted(ner_type_stats.items(), key=operator.itemgetter(1), reverse=True))
        ner_occurrences = dict(sorted(ner_occurrences.items(), key=operator.itemgetter(1), reverse=True))

        self.ner_stats = {
            "ner_type_stats": ner_type_stats,
            "ner_count": ner_count,
            "ner_coverage": round(ner_count / self.chars_count, 3),
            "ner_occurrences": ner_occurrences
        }

        del self.chars_count

        logger.debug("NER stats for single entry calculated")
