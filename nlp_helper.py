import spacy

from log_helper import create_logger_instance, create_file_for_logging, add_file_support_to_logger

allowed_ner_types = [
    'PERSON',
    'ORG',
    'GPE',
    'NORP',
    'WORK_OF_ART',
    'LAW',
    'PRODUCT',
    'LOC',
    'FAC',
    'EVENT',
    'MONEY',
    'LANGUAGE'
]

nlp = spacy.load('en_core_web_sm')


def get_stats_object():
    stats = {}

    for ner_type in allowed_ner_types:
        stats[ner_type] = 0

    return stats


def get_ner_infos_from_text(text):
    logger = create_logger_instance('nlp_application.NLP')
    file_handler = create_file_for_logging('debug.log')
    add_file_support_to_logger(logger, file_handler)

    logger.info("[SPACY] Start NLP processing single entry")
    doc = nlp(text)
    logger.info("[SPACY] Finish NLP processing single entry")

    entities = []
    entities_cpy = []

    stats = get_stats_object()

    logger.info("Start NER processing single entry")
    for entity in doc.ents:
        if entity.label_ not in allowed_ner_types:
            continue

        if entity.text not in entities_cpy:
            entities.append({
                'text': entity.text,
                'ner_label': entity.label_,
                'start': entity.start,
                'end': entity.end,
                'start_char': entity.start_char,
                'end_char': entity.end_char,
                'sent': entity.sent.text
            })
            stats[entity.label_] = stats[entity.label_] + 1

        entities_cpy.append(entity.text)
    logger.info("Finish NER processing single entry")

    return stats, entities
