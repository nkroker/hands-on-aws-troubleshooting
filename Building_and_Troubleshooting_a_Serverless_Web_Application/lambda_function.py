import boto3
import botocore
import random
import json
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    print("In lambda handler")

    # Generate a random fort_id
    fort_id = random.randint(1, 16)

    try:
        # Initialize DynamoDB resource
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table('fortunes')

        # Retrieve item from DynamoDB
        response = table.get_item(
            Key={'fort_id': fort_id},
            ProjectionExpression='fortune'
        )

        # Check if the item exists in the response
        if 'Item' in response:
            fortune = response['Item']['fortune']
        else:
            fortune = "Fortune not found"

        # Prepare response
        resp = {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps(fortune)
        }
    except Exception as e:
        # Handle exceptions
        print(f"Error: {e}")
        resp = {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

    return resp
