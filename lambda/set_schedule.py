import os
import boto3
from datetime import datetime
import uuid

TABLE_NAME = os.environ["TABLE_NAME"]
PRIMARY_KEY = os.environ["PRIMARY_KEY"]

def lambda_handler(event, context):
    dynamoDB = boto3.resource("dynamodb")
    table = dynamoDB.Table(TABLE_NAME) # DynamoDBのテーブル名

    timestamp = datetime.now()

    payload = event["body"]
    if (payload is None):
        return {
            "statusCode": 400,
            "body": "Error: You are missing the payload",
        }
    
    item = {
        PRIMARY_KEY: str(uuid.uuid4()),
        'interval': payload["interval"], # ex. 1 min/hour/day/week/year
        'date': payload["date"],
        'createdAt': timestamp,
        'updatedAt': timestamp,
    }

    try:
        dynamo.put_item(TableName=TABLE_NAME, Item=item)
        return { "statusCode": 200, "body": "Success" }
    except Exception as e:
        return { "statusCode": 500, "body": "Error" }