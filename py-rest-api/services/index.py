import json


# A simple handler
def handler(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps("Hello!"),
    }
