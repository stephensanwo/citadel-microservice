import json
from flask import jsonify
from mongoengine import *
from datetime import datetime
import os
import json


connect("citadel-microservice-dev-cluster", host="localhost", port=27017)


class Auth(Document):
    """
    Desc: Auth Schema for DB
    """

    # Personal Data
    client_desc = StringField(required=True)
    client_email = StringField(required=True)
    role = StringField(required=True)
    api_key = StringField(required=True)
    date_created = DateTimeField(default=datetime.utcnow)

    def auth_data(self):
        auth_dict = {
            "client_desc": self.client_desc,
            "client_email": self.client_email,
            "role": self.role,
            "date_created": self.date_created,
        }
        return auth_dict

    meta = {"indexes": ["client_email"], "ordering": ["-date_created"]}

