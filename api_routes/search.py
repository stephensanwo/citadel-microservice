from flask import Blueprint, request, make_response, jsonify
from .auth import require_apikey
from models.search.libgen import search_book
import logging
from database.SearchSchema import Search


LOG_FORMAT = "%(levelname)s %(asctime)s %(message)s"
logging.basicConfig(filename="./logs/search.log", level=logging.INFO, format=LOG_FORMAT)

logger = logging.getLogger()

search_blueprint = Blueprint("search", __name__)

# @route   GET /search
# @desc    Search for book in citadel API
# @access  Private
# @params  q=query string,


@search_blueprint.route("/search", methods=["GET"])
# @require_apikey
def search():
    q = request.args["q"]
    search_type = request.args["search_type"]

    Books = search_book(q, search_type)
    return make_response(jsonify(Books.records), int(Books.status["status_code"]))

    newSearch = Search(query=q, search_type=search_type, search_ip=request.remote_addr)
    newSearch.save()

    logger.error(f"API Key Authentication failed, Wrong API Client provided by user")

