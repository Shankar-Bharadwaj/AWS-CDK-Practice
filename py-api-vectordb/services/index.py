import json
from pinecone import Pinecone, ServerlessSpec
import os
import uuid


# Initialize a Pinecone client with your API key
api_key = os.environ.get("API_KEY")
pc = Pinecone(api_key=api_key)


# Create a dense index
index_name = "pinecone-db"
if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
        vector_type="dense",
        dimension=512,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        ),
        deletion_protection="disabled"
    )

index = pc.Index(host="https://pinecone-db-leohdy5.svc.aped-4627-b74a.pinecone.io")


def handler(event, context):
    print(json.dumps(event))
    method = event.get("httpMethod", "")

    if method == "POST":
        item = json.loads(event["body"])
        item["id"] = str(uuid.uuid4())

        # Removing 'vector' from metadata
        metadata = {k: v for k, v in item.items() if k != "vector"}

        index.upsert(
            vectors=[
                {
                    "id": item["id"],
                    "values": item["vector"],
                    "metadata": metadata
                }
            ],
            namespace="example-db"
        )

        return {
            "statusCode": 200,
            "body": json.dumps({"id": item["id"]}),
        }
    
    if method == "GET":
        vector_id = event["queryStringParameters"]["id"]
        response = index.fetch(ids=[vector_id], namespace="example-db")
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
