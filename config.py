PLATO_ROOT_URL = "https://plato.stanford.edu"
PLATO_TOC_URL = f"{PLATO_ROOT_URL}/contents.html"
PLATO_LOG_FILE_NAME = "logs/plato"
PLATO_LOG_FILE_EXTENSION = "log"
PLATO_NLP_PIPELINE = "en_core_web_sm"
PLATO_DBPEDIA_URL = "http://dbpedia.org/sparql"
PLATO_SPARQL_QUERY_FOR_GETTING_TYPE_PROPS = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?prop (COUNT(DISTINCT ?instance) AS ?count) WHERE {{
    ?instance a {0};
    ?prop ?name
}} ORDER BY DESC(?count)
"""
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
    "DBPEDIA_TYPES": "dbpedia_types"
}
PLATO_STATS_IDS = {
    "OVERALL_NER_STATS": "overall_ner_stats"
}
