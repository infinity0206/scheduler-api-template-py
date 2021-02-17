import os
import boto3
import json

TABLE_NAME = os.environ["TABLE_NAME"]
PRIMARY_KEY = os.environ["PRIMARY_KEY"]

def lambda_handler(event, context):
    dynamoDB = boto3.resource("dynamodb")
    table = dynamoDB.Table(TABLE_NAME) # DynamoDBのテーブル名

    if (event["pathParameters"] is not None and event["pathParameters"]["id"] is not None):
        return get_schedule(event["pathParameters"]["id"], table)
    else:
        return get_schedules(table)

def get_schedule(id, table):
    try:
        res = table.get_item(Key={'id': id})
        if("Item" not in res.keys() or res['Item'] is None):
            return {
                'statusCode': 200,
                'headers': {},
                'body': json.dumps({}),
                'isBase64Encoded': False
            }
        return {
                'statusCode': 200,
                'headers': {},
                'body': json.dumps(res["Item"]),
                'isBase64Encoded': False
            }
    except Exception as e:
        return {
                'statusCode': 500,
                'headers': {},
                'body': 'Error',
                'isBase64Encoded': False
            }

def get_schedules(table):
    try:
        res = table.scan()
        if(res['Item'] is None):
            return []
        return res["Item"]
    except Exception as e:
        return 'Error'