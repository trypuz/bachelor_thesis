import spacy
import logging

from config import PLATO_NLP_PIPELINE

logger = logging.getLogger(__name__)


class NLP:
    def __init__(self, text):
        self._text = text
        self._nlp = spacy.load(PLATO_NLP_PIPELINE)
        self._doc = self._nlp(self._text)

    def get_ner_info(self):
        logger.debug("Starting extract NER results from single entry")
        ner_info = []

        for entity in self._doc.ents:
            ner_info.append({
                "text": entity.text,
                "start_char": entity.start_char,
                "end_char": entity.end_char,
                "label": entity.label_
            })

        logger.debug("NER results from single entry extracted")

        return ner_info

