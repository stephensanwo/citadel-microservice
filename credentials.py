import sys
import bcrypt
import logging
import uuid
from database.AuthSchema import Auth

LOG_FORMAT = "%(levelname)s %(asctime)s %(message)s"
logging.basicConfig(
    filename="./logs/api-authentication-credentials.log",
    level=logging.INFO,
    format=LOG_FORMAT,
)

logger = logging.getLogger()


def create_api_credentials():
    client_desc = str(sys.argv[1])
    client_email = str(sys.argv[2])
    role = str(sys.argv[3])
    api_key = str(uuid.uuid4())

    print(
        f"""
        Your Credentials
        ------------------
        User: {client_desc}
        Email: {client_email}  
        API Key: {api_key}
        ------------------

        Please keep your crednetials safe and create a record as this cannot be retrieved if lost
        """
    )
    logger.info(f"API Credentials generated for {client_email}")

    logger.info(f"User: {client_desc}, Email: {client_email}, API Key: {api_key}")

    # Hashing API credentials for the DB
    api_key = bcrypt.hashpw(api_key.encode("utf-8"), bcrypt.gensalt())

    logger.info(f"API Key Hashed: {api_key}")

    api_credentials = Auth(
        client_desc=client_desc, role=role, client_email=client_email, api_key=api_key,
    )
    api_credentials.save()

    logger.info("API Credentials stored in Auth databse")
    logger.info("API Credentials Created Successfully")
    return "API Credentials Created Successfully"


create_api_credentials()

# Example in CLI
# python credentials.py admin-stephen-sanwo stephen.sanwo@icloud.com admin
