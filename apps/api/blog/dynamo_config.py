"""
DynamoDB configuration for PynamoDB models
"""

import os
from decouple import config

# AWS Configuration
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID', default='')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY', default='')
AWS_REGION = config('AWS_REGION', default='us-east-1')

# DynamoDB Local configuration (for development)
DYNAMODB_LOCAL_HOST = config('DYNAMODB_LOCAL_HOST', default='http://localhost:8000')
USE_DYNAMODB_LOCAL = config('USE_DYNAMODB_LOCAL', default=False, cast=bool)

# Table name prefix (useful for different environments)
TABLE_PREFIX = config('DYNAMODB_TABLE_PREFIX', default='cgstewart_')

def configure_pynamodb():
    """Configure PynamoDB with environment settings"""
    if USE_DYNAMODB_LOCAL:
        # For local development with DynamoDB Local
        os.environ['AWS_ACCESS_KEY_ID'] = 'fake'
        os.environ['AWS_SECRET_ACCESS_KEY'] = 'fake'
        # PynamoDB will use the host setting from model Meta classes
    else:
        # For AWS DynamoDB
        if AWS_ACCESS_KEY_ID:
            os.environ['AWS_ACCESS_KEY_ID'] = AWS_ACCESS_KEY_ID
        if AWS_SECRET_ACCESS_KEY:
            os.environ['AWS_SECRET_ACCESS_KEY'] = AWS_SECRET_ACCESS_KEY
        if AWS_REGION:
            os.environ['AWS_DEFAULT_REGION'] = AWS_REGION

# Call this when the app starts
configure_pynamodb()
