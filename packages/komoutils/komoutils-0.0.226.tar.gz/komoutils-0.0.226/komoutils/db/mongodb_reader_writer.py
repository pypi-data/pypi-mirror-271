import logging
from typing import Union

import pymongo

from komoutils.core import KomoBase


class MongoDBReaderWriter(KomoBase):

    def __init__(self, uri: str, db_name: str):
        self.client: pymongo.MongoClient = pymongo.MongoClient(uri)
        self.db = self.client[db_name]

    @property
    def name(self):
        return "mongodb_reader_writer"

    def start(self):
        pass

    def read(self, collection: str, filters=None, omit=None, limit: int = 1000000):
        if filters is None:
            filters = {}
        if omit is None:
            omit = {}

        records: list = list(self.db[collection].find(filters, omit).sort('_id', -1).limit(limit=limit))
        return records

    def write(self, collection: str, data: Union[list, dict]):
        if len(data) == 0:
            self.log_with_clock(log_level=logging.INFO,
                                msg=f"0 records to send for collection {collection}. ")
            return
        # print(f"++++++++++++++++++++++++++++++++++++++++++++++++")
        try:
            if isinstance(data, dict):
                self.db[collection].insert_one(data)
            elif isinstance(data, list):
                self.db[collection].insert_many(data)

            self.log_with_clock(log_level=logging.DEBUG, msg=f"Successfully sent {collection} with size "
                                                             f"{len(data)} data to database. ")
            return 'success'
        except Exception as e:
            self.log_with_clock(log_level=logging.ERROR, msg=f"Unspecified error occurred. {e}. ")

    def updater(self, collection: str, filters: dict, updater: dict):
        if len(updater) == 0:
            self.log_with_clock(log_level=logging.INFO,
                                msg=f"0 records to send for {self.db.upper()} for collection {collection}. ")
            return

        result = self.db[collection].update_one(filter=filters, update=updater, upsert=True)
        return result

    def check_if_collection_exists(self, collection_name: str):
        return self.db.list_collection_names().count(collection_name) > 0

    def create_collection(self, collection_name: str, indexes: list = [], create_ttl: int = 0):
        # Check if collection exists
        collection_exists = self.db.list_collection_names().count(collection_name) > 0

        if not collection_exists:
            collection = self.db[collection_name]
            self.log_with_clock(log_level=logging.INFO, msg=f"Collection {collection_name} has been created. ")

        # Create ttl index id ordered
        ttl_field = "timestamp"  # Field used for expiration check
        if create_ttl > 0:
            # Define the field and expiration time for TTL
            expire_after_seconds = create_ttl  # Documents expire after 1 hour (adjust as needed)

            # Check if the TTL index already exists
            existing_indexes = self.db[collection_name].index_information()
            has_ttl_index = False
            for index in existing_indexes.values():
                if index.get("name") == f"{ttl_field}_1" and index.get("expireAfterSeconds") == expire_after_seconds:
                    has_ttl_index = True
                    break

            # Create TTL index if it doesn't exist
            if not has_ttl_index:
                self.db[collection_name].create_index([(ttl_field, pymongo.ASCENDING)],
                                                      expireAfterSeconds=expire_after_seconds)
                self.log_with_clock(log_level=logging.INFO,
                                    msg=f"TTL index created on '{ttl_field}' with expireAfterSeconds: {expire_after_seconds}")

        # Create indexes only if collection exists
        for field_to_index in indexes:
            if field_to_index == ttl_field and create_ttl is True:
                self.log_with_clock(log_level=logging.WARNING, msg=f"Omitting TTL field {field_to_index}. ")
                continue

            # collection = self.db[collection_name]
            self.db[collection_name].create_index([(field_to_index, pymongo.ASCENDING)])
            self.log_with_clock(log_level=logging.INFO,
                                msg=f"Index created on '{field_to_index}' in collection '{collection_name}'. ")

    def remove_collection(self, collection_name: str):
        collection_exists = self.db.list_collection_names().count(collection_name) > 0

        if not collection_exists:
            self.log_with_clock(log_level=logging.INFO,
                                msg=f"Collection {collection_name} does not exist. {collection_exists}")
            return

        self.db.drop_collection(collection_name)
        self.log_with_clock(log_level=logging.INFO, msg=f"Collection '{collection_name}' has been removed. ")

    def get_all_collections(self):
        return self.db.list_collection_names()
