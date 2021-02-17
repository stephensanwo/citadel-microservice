from flask import Blueprint, request, make_response, jsonify
from .auth import require_apikey
from models.search.libgen import search_book
from api_config import search_queries_db
import logging
import datetime
import uuid


LOG_FORMAT = "%(levelname)s %(asctime)s %(message)s"
logging.basicConfig(filename="./logs/search.log",
                    level=logging.INFO,
                    format=LOG_FORMAT)

logger = logging.getLogger()

search_blueprint = Blueprint('search', __name__)

# @route   GET /search
# @desc    Search for book in citadel API
# @access  Private
# @params  q=query string, 

@search_blueprint.route('/search', methods=['POST'])
@require_apikey
def search():
    q = request.form['q']
    search_type = request.form['search_type']

    search_queries_db.put_item(
        Item={
            "search_query": q,
            "search_type": search_type,
            "search_ip": request.remote_addr,
            "search_time": str(datetime.datetime.now()),
            "search_id": str(uuid.uuid4())
        })


    Books = search_book(q, search_type)
    logger.error(f"API Key Authentication failed, Wrong API Client provided by user")
    
    return make_response(jsonify(Books.records), int(Books.status['status_code'])) 