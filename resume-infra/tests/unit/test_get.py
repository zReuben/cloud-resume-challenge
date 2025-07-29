# Import standard modules
import os
import json
import boto3

# Import Moto to mock AWS services like DynamoDB
from moto import mock_dynamodb

# Import the handler to test
from functions.get.handler import handler  # adjust if you renamed it


# This decorator mocks all DynamoDB calls inside the test
@mock_dynamodb
def test_get_handler():
    # Setup env var used by your Lambda function
    os.environ["TABLE_NAME"] = "VisitorTable"

    # Create mock DynamoDB table (doesn't hit real AWS)
    ddb = boto3.resource("dynamodb", region_name="us-east-1")
    table = ddb.create_table(
        TableName="VisitorTable",
        KeySchema=[{"AttributeName": "ID", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "ID", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST"
    )

    # Wait for mock table to be "ready"
    table.meta.client.get_waiter('table_exists').wait(TableName="VisitorTable")
    
    # Insert mock item in the fake table
    table.put_item(Item={"ID": "visitorCount", "count": 123})

    # Create a fake API Gateway event that mimics a GET request
    event = {"httpMethod": "GET"}

    # Call your Lambda function handler
    response = handler(event, context={})

    #TEMP ADDITION FOR TROUBLESHOOTING:
    print("Lambda response:", response)

    # Basic checks
    assert response["statusCode"] == 200

    # Parse the returned JSON body and check if count is correct
    body = json.loads(response["body"])
    assert body["count"] == 123

