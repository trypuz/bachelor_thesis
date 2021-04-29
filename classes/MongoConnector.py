import logging
import pymongo

from config import PLATO_MONGO_DB_NAME, PLATO_MONGO_COLLECTIONS
from classes.EntryModel import EntryModel
from classes.StatsModel import StatsModel
from classes.NerResultsModel import NerResultsModel

logger = logging.getLogger(__name__)


class MongoConnector:
    def __init__(self, url):
        logger.debug(f"Starting connect to MongoDB using url: {url}")
        self.mongo_handler = pymongo.MongoClient(url)
        logger.debug("Connected to MongoDB successfully")

        db_list = self.mongo_handler.list_database_names()

        if PLATO_MONGO_DB_NAME in db_list:
            logger.debug(f"{PLATO_MONGO_DB_NAME} db already exists, so no action is required")
        else:
            logger.debug(f"{PLATO_MONGO_DB_NAME} db not exists, so will be created")

        self.db = self.mongo_handler[PLATO_MONGO_DB_NAME]
        self.collections = {}

        collection_list = self.db.list_collection_names()

        for collection_name in PLATO_MONGO_COLLECTIONS.values():
            if collection_name not in collection_list:
                logger.debug(f"{collection_name} collection not exists, so will be created")
            else:
                logger.debug(f"{collection_name} collection already exists, so no action is required")

            self.collections[collection_name] = self.db[collection_name]

    def add_entry_to_collection(self, entry_model: EntryModel):
        self.collections[PLATO_MONGO_COLLECTIONS["ENTRIES"]].insert_one(vars(entry_model))

    def get_all_entries_from_collection(self):
        logger.debug("Getting all entries from DB")
        entries = self.collections[PLATO_MONGO_COLLECTIONS["ENTRIES"]].find()
        logger.debug("All entries from DB retrieved")
        return entries

    def get_all_ner_results_from_collection(self):
        logger.debug("Getting all NER results from DB")
        ner_results = self.collections[PLATO_MONGO_COLLECTIONS["NER"]].find()
        logger.debug("All NER results retrieved")
        return ner_results

    def get_overall_stats_by_id(self, stats_id):
        overall_stats = self.collections[PLATO_MONGO_COLLECTIONS["STATS"]].find_one({"stats_id": stats_id})
        return overall_stats

    def add_ner_results_for_single_entry_to_collection(self, ner_results_model: NerResultsModel):
        self.collections[PLATO_MONGO_COLLECTIONS["NER"]].insert(vars(ner_results_model))

    def add_stats_to_collection(self, stats_model: StatsModel):
        self.collections[PLATO_MONGO_COLLECTIONS["STATS"]].insert_one(vars(stats_model))
