import os
import json
import boto3
from moto import mock_dynamodb
from functions.put.handler import handler

@mock_dynamodb
def test_put_handler():
    os.environ["TABLE_NAME"] = "VisitorTable"
    ddb = boto3.resource("dynamodb", region_name="us-east-1")
    table = ddb.create_table(
        TableName="VisitorTable",
        KeySchema=[{"AttributeName": "ID", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "ID", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST"
    )
    table.meta.client.get_waiter('table_exists').wait(TableName="VisitorTable")
    table.put_item(Item={"ID": "visitorCount", "count": 5})

    event = {"httpMethod": "PUT", "body": json.dumps({})}
    response = handler(event, context={})

    assert response["statusCode"] == 204
    assert "body" not in response

