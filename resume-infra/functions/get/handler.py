import os, json, boto3

# This is the GET handler

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

cors_headers = {
    'Access-Control-Allow-Origin': 'https://reubenmulholland.com',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
}

def handler(event, context):
    
    try:
        response = table.get_item(Key={'ID': 'visitorCount'})
        count = response.get('Item', {}).get('count', 0)

        return {
            'statusCode': 200,
            'headers': cors_headers,
            'body': json.dumps({'count': int(count)})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': cors_headers,
            'body': json.dumps({'error': str(e)})
        }
