# Module to import json data into dynamodb database

import boto3
import json

business_map = {}

with open("yelp_academic_dataset_business.json", "r") as f:
    for line in f:
        item = json.loads(line)
        
        business_map[item["business_id"]] = item["name"]

print(json.dumps(business_map, indent=2))

# Constants for table names and batch size
table_name = "business_review"
batch_size = 25  # DynamoDB batch write size limit

ddb_client = boto3.client("dynamodb", region_name="us-west-1")

# Prepare batch input list
batch_input = []

# Open and stream the large JSON file using ijson to reduce memory usage
with open("yelp_academic_dataset_review.json", "r") as f:
    # Stream JSON data with ijson to avoid loading full lines into memory
    for line in f:
        review = json.loads(line)
        
        # Append each parsed business to the batch_input list
        batch_input.append({
            "PutRequest": {
                "Item": {
                    "business_id": {"S": review["business_id"]},
                    "business_name": {"S": business_map[review["business_id"]]},
                    "review_id": {"S": review["review_id"]},
                    "text": {"S": review["text"]},
                    "user_id": {"S": review["user_id"]},
                }
            }
        })
        
        # Once the batch_input list reaches the batch_size, send the batch request
        if len(batch_input) == batch_size:
            # Batch write into DynamoDB
            response = ddb_client.batch_write_item(
                RequestItems={table_name: batch_input}
            )
            # Clear batch_input after the batch write
            batch_input = []

    # Handle any remaining items not written in the last batch
    if batch_input:
        response = ddb_client.batch_write_item(
            RequestItems={table_name: batch_input}
        )
        