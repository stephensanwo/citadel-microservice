import sys
from config import api_credentials_db
import uuid
import bcrypt
import logging


LOG_FORMAT = "%(levelname)s %(asctime)s %(message)s"
logging.basicConfig(filename="../logs/api-authentication-credentials.log",
                    level=logging.INFO,
                    format=LOG_FORMAT)

logger = logging.getLogger()


def create_api_credentials():
    client_desc = str(sys.argv[1])
    client_email = str(sys.argv[2])
    role = str(sys.argv[3])
    client_id = str(uuid.uuid4())
    api_key = str(uuid.uuid4())

    print(f"""
        Your Credentials
        ------------------
        User: {client_desc}
        Email: {client_email}  
        Client ID: {client_id}
        API Key: {api_key}
        ------------------

        Please keep your crednetials safe and create a record as this cannot be retrieved if lost
        """
          )
    logger.info(f"API Credentials generated for {client_email}")
    logger.info(
        f"User: {client_desc}, Email: {client_email}, Client ID: {client_id}, API Key: {api_key}")

    # Hashing API credentials for the DB
    api_key = bcrypt.hashpw(api_key.encode('utf-8'), bcrypt.gensalt())

    logger.info(f"API Key Hashed: {api_key}")

    api_credentials_db.put_item(
        Item={
            "api_client": client_id,
            "api_key": api_key.decode('utf-8'),
            "client_desc": client_desc,
            "client_email": client_email,
            "role": role
        })

    logger.info("API Credentials stored in databse")
    logger.info("API Credentials Created Successfully")
    return "API Credentials Created Successfully"


create_api_credentials()

# Example in CLI
# python credentials.py admin-stephen-sanwo stephen.sanwo@icloud.com admin
