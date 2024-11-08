import boto3
import json
from decimal import Decimal #import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('VisitorCount')  # Replace 'VisitorCount' if your table name is different

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)  # Convert Decimal to float for JSON serialization
    raise TypeError("Type not serializable")

def lambda_handler(event, context):
    response = table.update_item(
        Key={'id': 'count'},
        UpdateExpression="ADD visit_count :inc",
        ExpressionAttributeValues={':inc': 1},
        ReturnValues="UPDATED_NEW"
    )

    
    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps(response['Attributes']['visit_count'],default=decimal_default)
    }

