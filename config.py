PLATO_ROOT_URL = "https://plato.stanford.edu"
PLATO_TOC_URL = f"{PLATO_ROOT_URL}/contents.html"
PLATO_LOG_FILE_NAME = "logs/plato"
PLATO_LOG_FILE_EXTENSION = "log"
PLATO_NLP_PIPELINE = "en_core_web_lg"
PLATO_DBPEDIA_URL = "http://dbpedia.org/sparql"
PLATO_NER_ALLOWED_TYPES = [
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
PLATO_NER_TO_DBPEDIA_TYPES_MAP = {
    'PERSON': 'dbo:Person',
    'ORG': 'dbo:Company',
    'GPE': 'dbo:Location',
    'NORP': 'dbo:Country',
    'WORK_OF_ART': 'dbo:Work',
    'LAW': '',
    'PRODUCT': '',
    'LOC': '',
    'FAC': '',
    'EVENT': 'dbo:Event',
    'MONEY': 'dbo:Currency',
    'LANGUAGE': 'dbo:Language'
}
PLATO_MONGO_URL = "mongodb://localhost:27017/"
PLATO_MONGO_DB_NAME = "plato"
PLATO_MONGO_COLLECTIONS = {
    "ENTRIES": "entries",
    "NER": "ner_results",
    "STATS": "stats",
}
PLATO_STATS_IDS = {
    "OVERALL_NER_TYPE_STATS": "overall_ner_type_stats",
    "OVERALL_NER_COUNT_STATS": "overall_ner_count_stats",
    "OVERALL_WORDS_COUNT_STATS": "overall_words_count_stats",
    "OVERALL_NER_COVERAGE_STATS": "overall_ner_coverage_stats",
    "OVERALL_NER_OCCURRENCES_STATS": "overall_ner_occurrences_stats"
}
