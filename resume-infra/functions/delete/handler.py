import os, json, boto3

# This is the DELETE handler

cors_headers = {
    'Access-Control-Allow-Origin': 'https://reubenmulholland.com',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,DELETE'
}

def handler(event, context):
    
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table(os.environ['TABLE_NAME'])
    try:
        table.delete_item(Key={'ID': 'visitorCount'})
        return {
            'statusCode': 204,
            'headers': cors_headers
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': cors_headers,
            'body': json.dumps({'error': str(e)})
        }

