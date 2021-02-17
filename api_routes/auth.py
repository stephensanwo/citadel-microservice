from flask import Blueprint, jsonify, make_response
from functools import wraps
from flask import request, abort
from api_config import api_credentials_db
import bcrypt
import logging


LOG_FORMAT = "%(levelname)s %(asctime)s %(message)s"
logging.basicConfig(filename="./logs/api-key-authentication.log",
                    level=logging.INFO,
                    format=LOG_FORMAT)

logger = logging.getLogger()

auth_blueprint = Blueprint('auth', __name__)

def vaidate_api_credentials(api_key, api_client):
    """
    Match API key
    @param api_key: API key from request
    @param api_client: API Client from request.
    @return: boolean
    """
    if api_key is None or api_client is None:
        logger.error(f"API Key Authentication failed, API Key or API Client not provided by user")
        return False
    try:
        # Find the client ID provided from the credentials DB              
        client = api_credentials_db.get_item(Key={'api_client': api_client})
        # Get the Hashed API key for the client_id from the DB and unhash with bcrypt
        hashed_api_key = client["Item"]['api_key']
        user = client["Item"]['client_desc']
    except:
        logger.error(f"API Key Authentication failed, Wrong API Client provided by user")
        return False

    if bcrypt.checkpw(api_key.encode('utf-8'), hashed_api_key.encode('utf-8')):
        logger.info(f"API Key Authenticated for user {user}")
        return True

    logger.error(f"API Key Authentication failed, Wrong API Key provided by user")
    return False



# Decorator for requiring api key on routes
def require_apikey(function):
    """
    @param function: function
    @return: decorator, return the wrapped function or abort json object.
    """
    @wraps(function)
    def decorated_function(*args, **kwargs):
        api_key = request.headers['api_key']
        api_client = request.headers['api_client']

        if vaidate_api_credentials(api_key, api_client):
            return function(*args, **kwargs)
        else:
            logger.warning(f"Unauthorized address trying to use API: {request.remote_addr}")
            abort(401)

    return decorated_function



#Test

# @route   GET /auth
# @desc    Test
# @access  Public - Test Only
@auth_blueprint.route('/auth')
@require_apikey
def auth_user():
    auth_status = "Authenticated!"
    return make_response(jsonify(auth_status), 200)

