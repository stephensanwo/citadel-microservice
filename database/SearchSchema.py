import json
from flask import jsonify
from mongoengine import *
from datetime import datetime
import os
import json


connect("citadel-microservice-dev-cluster", host="localhost", port=27017)


class Search(Document):
    """
    Desc: Books Schema for DB
    """

    # Personal Data
    query = StringField(required=True)
    search_type = StringField(required=True)
    search_ip = StringField(required=True)
    search_time = DateTimeField(default=datetime.utcnow)

    def search_data(self):
        search_dict = {
            "query": self.query,
            "search_type": self.search_type,
            "search_ip": self.search_ip,
            "search_time": self.search_time,
        }
        return search_dict

    meta = {"indexes": ["query"], "ordering": ["-search_time"]}
