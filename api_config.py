# PATH Configuration Files
import os
import boto3
import s3fs

# Local

# AWS S3 Bucket Config
CITADEL_STORAGE = os.environ.get("CITADEL_STORAGE")
AWS_KEY = os.environ.get("AWS_KEY")
AWS_SECRET = os.environ.get("AWS_SECRET")
API_CREDENTIALS_DB = os.environ.get("API_CREDENTIALS_DB")
SEARCH_QUERIES_DB = os.environ.get("SEARCH_QUERIES_DB")

# S3 bucket init

s3 = boto3.client('s3', aws_access_key_id=AWS_KEY,
                  aws_secret_access_key=AWS_SECRET)


s3_resource = boto3.resource('s3')
citadel_storage = s3_resource.Bucket(CITADEL_STORAGE)


# Dynamo DB init

dynamodb = boto3.resource('dynamodb', aws_access_key_id=AWS_KEY,
                          aws_secret_access_key=AWS_SECRET,  region_name='us-east-2')


api_credentials_db = dynamodb.Table(API_CREDENTIALS_DB)
search_queries_db = dynamodb.Table(SEARCH_QUERIES_DB)


# S3fs

s3fs_object = s3fs.S3FileSystem(anon=False, key=AWS_KEY, secret=AWS_SECRET)


# Base URLs for Search API

BASE_URL = os.environ.get("base_url")
BASE_URL1 = os.environ.get("base_url1")