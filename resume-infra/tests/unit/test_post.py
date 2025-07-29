import os
import json
import boto3
from moto import mock_dynamodb
from functions.post.handler import handler


@mock_dynamodb
def test_post_handler():
    os.environ["TABLE_NAME"] = "VisitorTable"
    ddb = boto3.resource("dynamodb", region_name="us-east-1")
    table = ddb.create_table(
        TableName="VisitorTable",
        KeySchema=[{"AttributeName": "ID", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "ID", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST"
    )
    table.meta.client.get_waiter('table_exists').wait(TableName="VisitorTable")

    # Simulate POST event
    event = {"httpMethod": "POST"}

    response = handler(event, context={})
    body = json.loads(response["body"])

    assert response["statusCode"] == 200
    assert "message" in body or "count" in body  # Adjust depending on what your POST returns

