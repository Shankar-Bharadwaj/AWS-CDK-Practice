import json
from pinecone import Pinecone, ServerlessSpec
import os
import uuid
import time


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
    # print(json.dumps(event))
    path = event["resource"]
    method = event["httpMethod"]

    if path == "/vector" and method == "POST":
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
    
    elif path == "/vector" and method == "GET":
        vector_id = event["queryStringParameters"]["id"]
        response = index.fetch(ids=[vector_id], namespace="example-db")

        if vector_id in response.vectors:
            return {
                "statusCode": 200,
                "body": json.dumps(response.vectors[vector_id].to_dict()),
            }
        else:
            return {
                "statusCode": 404,
                "body": json.dumps({"message": "Not Found"}),
            }
        
    elif path == "/query" and method == "POST":
        body = json.loads(event["body"])
        query_vector = body["vector"]
        top_k = body.get("top_k", 1)

        start_time = time.perf_counter()
        query_result = index.query(
            namespace="example-db",
            vector=query_vector,
            top_k=top_k,
            include_metadata=True,
            include_values=False
        )
        latency = time.perf_counter() - start_time

        return {
            "statusCode": 200,
            "body": json.dumps({
                "matches": query_result.to_dict(),
                "query_latency_ms": round(latency * 1000, 2)
            })
        }

    else:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Unsupported route or method"})
        }