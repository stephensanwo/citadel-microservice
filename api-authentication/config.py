# PATH Configuration Files
import os
import boto3


# AWS Config
AWS_KEY = os.environ.get("AWS_KEY")
AWS_SECRET = os.environ.get("AWS_SECRET")
API_CREDENTIALS_DB = os.environ.get("API_CREDENTIALS_DB")

# Dynamo DB init

dynamodb = boto3.resource('dynamodb', aws_access_key_id=AWS_KEY,
                          aws_secret_access_key=AWS_SECRET,  region_name='us-east-2')


api_credentials_db = dynamodb.Table(API_CREDENTIALS_DB)
