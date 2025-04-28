import json
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.models import Distance, VectorParams
import os
import uuid
import time


# ************************************* QDRANT DB *************************************************

# Initialize a Qdrant client with your API key
api_key = os.environ.get("API_KEY")

qdrant_client = QdrantClient(
    url="https://44e1e7af-fed6-47ae-a257-52a167d242c1.us-east-1-0.aws.cloud.qdrant.io", 
    api_key=api_key
)

if not qdrant_client.collection_exists(collection_name="test_collection"):
    qdrant_client.create_collection(
        collection_name="test_collection",
        vectors_config=VectorParams(size=512, distance=Distance.COSINE)
    )


def handler(event, context):
    path = event["resource"]
    method = event["httpMethod"]

    if path == "/qdrant" and method == "POST":
        item = json.loads(event["body"])
        item["id"] = str(uuid.uuid4())

        # Removing 'vector' from metadata
        metadata = {k: v for k, v in item.items() if k != "vector"}

        qdrant_client.upsert(
            collection_name = "test_collection",
            points = models.Batch(
                ids = [item["id"]],
                vectors = [item["vector"]],
                payloads = [metadata]
            )
        )

        return {
            "statusCode": 200,
            "body": json.dumps({"id": item["id"]}),
        }
    
    elif path == "/query_qdrant" and method == "POST":
        body = json.loads(event["body"])
        query_vector = body["vector"]
        limit = body.get("limit", 1)

        start_time = time.perf_counter()
        query_result = qdrant_client.query_points(
            collection_name="test_collection",
            query=query_vector,
            limit=limit
        ).points
        latency = time.perf_counter() - start_time

        return {
            "statusCode": 200,
            "body": json.dumps({
                "matches": [point.dict() for point in query_result],
                "query_latency_ms": round(latency * 1000, 2)
            })
        }

    else:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Unsupported route or method"})
        }
