import json
import boto3
import os
import uuid

# Get the database client outside of the handler functions to prevent redundancy
table_name = os.environ.get("TABLE_NAME")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(table_name)


# A simple handler
# def handler(event, context):
#     return {
#         "statusCode": 200,
#         "body": json.dumps("Hello!"),
#     }


# Handler for our RestAPI
def handler(event, context):
    method = event["httpMethod"]

    if method == "POST":
        item = json.loads(event["body"])
        item["id"] = str(uuid.uuid4())
        table.put_item(Item=item)
        return {
            "statusCode": 200,
            "body": json.dumps({"id": item["id"]}),
        }
    if method == "GET":
        empl_id = event['queryStringParameters']['id']
        response = table.get_item(
            Key = {
                "id":empl_id
            }
        )
        if "Item" in response:
            return {
                "statusCode": 200,
                "body": json.dumps(response['Item']),
            }
        else:
            return {
                "statusCode": 404,
                "body": json.dumps("Not Found"),
            }
