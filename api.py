import os
from flask import Flask, Blueprint
from api_routes.search import search_blueprint
from api_routes.auth import auth_blueprint

api = Flask(__name__)
api.register_blueprint(auth_blueprint)
api.register_blueprint(search_blueprint)


if __name__ == "__main__":

    api.run()
