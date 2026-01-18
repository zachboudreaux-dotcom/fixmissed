import json
import uuid
import boto3
from datetime import datetime, timezone

dynamodb = boto3.resource("dynamodb")
import os
table = dynamodb.Table(os.environ["TABLE_NAME"])


def lambda_handler(event, context):
    body = event.get("body")
    if not body:
        return {"statusCode": 400, "body": "No body received"}

    try:
        data = json.loads(body)

        item = {
            "leadId": str(uuid.uuid4()),
            "from": data.get("from"),
            "message": data.get("message"),
            "createdAt": datetime.now(timezone.utc).isoformat()
        }

        table.put_item(Item=item)
        print("Saved item:", item)

        return {"statusCode": 200, "body": "Saved"}

    except Exception as e:
        print("ERROR:", str(e))
        return {"statusCode": 500, "body": "Internal Server Error"}
