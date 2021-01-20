from functools import reduce

from file_helper import write_to_json
from object_helper import sum_dictionaries, sort_stats_from_largest
from nlp_helper import get_ner_infos_from_text
from solr_helper import connect_to_platform
from log_helper import create_logger_instance, create_file_for_logging, add_file_support_to_logger
from string_helper import remove_special_chars_from_text, change_whitespaces_to_dash

logger = create_logger_instance('nlp_application.MAIN')
file_handler = create_file_for_logging('debug.log')
add_file_support_to_logger(logger, file_handler)

logger.info("Starting connect to Apache Solr database")
solr_conn = connect_to_platform('http://localhost:8983/solr/main_core')
logger.info("Connect to Apache Solr database finished")

logger.info("Start data searching in Apache Solr database")
results = solr_conn.search(q='*:*', rows=2147483647)
logger.info("Data searching has just ended")

data = {}

all_stats = []

logger.info("NLP DATA PROCESSING HAS JUST STARTED")
for result in results:
    title = result['title'][0]
    preamble = result['preamble'][0]
    main_text = result['main_text'][0]
    whole_content = preamble + main_text

    logger.info("Remove special chars from title has started")
    title = remove_special_chars_from_text(title)
    logger.info("Remove special chars from title has finished")
    logger.info("Change whitespaces to dash has started")
    title = change_whitespaces_to_dash(title)
    logger.info("Change whitespaces to dash has finished")
    logger.info("Transform to lowercase has started")
    title = title.lower()
    logger.info("Transform to lowercase has finished")

    logger.info("Getting NER info from encyclopedia entry has started")
    stats_results, ner_results = get_ner_infos_from_text(whole_content)
    logger.info("Getting NER info from encyclopedia entry has finished")

    logger.info("Adding NER stats to statistics set")
    all_stats.append(stats_results)
    logger.info("NER stats added to statistics")

    data[title] = {
        'stats': sort_stats_from_largest(stats_results),
        'ner': ner_results
    }
logger.info("NLP DATA PROCESSING HAS JUST ENDED")

logger.info("Creating new file and add stats to its")
write_to_json("data.json", data)
logger.info("File creation with statistics has just ended")

logger.info("Merge all NER statistics to make overall stats")
sum_stats = reduce(sum_dictionaries, all_stats, {})
logger.info("NER stats merged")
logger.info("Sort overall stats from largest")
sum_stats = sort_stats_from_largest(sum_stats)
logger.info("Overall stats sorted")

logger.info("Creating file with overall stats")
write_to_json("stats.json", sum_stats)
logger.info("File with overall stats created")
