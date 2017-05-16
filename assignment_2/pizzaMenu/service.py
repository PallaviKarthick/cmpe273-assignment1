import boto3
import json
from boto3 import dynamodb
from boto3.session import Session


db_session = Session(aws_access_key_id='*****' , aws_secret_access_key='*****',region_name='us-west-1')
dynamodb = db_session.resource('dynamodb')
menu_table = dynamodb.Table('Menu')

def handler(event, context):
    method_type = event['httpMethod']
    if method_type=='POST':
        menuId=event['body']['menu_id']
        response = menu_table.put_item(
            Item = {
                "menu_id": event['body']['menu_id'],
                "store_name" :event['body']['store_name'],
                "selection" :event['body']['selection'],
                "size" :event['body']['size'],
                "price" :event['body']['price'],
                "store_hours" :event['body']['store_hours']

            })
        return "POSTED with menu_id: "+menuId
    elif method_type=='GET' :
        response = menu_table.get_item(
            Key={
                "menu_id":event['body']['menu_id']
            })
        return response['Item']
    elif method_type=='DELETE' :
        menu_table.delete_item(
            Key={
                "menu_id":event['body']['menu_id']
            })
        return "DELETED"
    elif method_type=='PUT' :
        attr = event['body'].keys()
        for k in attr:
            if str(k)!='menu_id':
                menu_table.update_item(
                  Key={
                "menu_id":event['body']['menu_id']},
                UpdateExpression ='set ' + str(k) + '= :s', ExpressionAttributeValues={
                    ':s' : event['body'][str(k)]
                })
        return "UPDATED"
    else :
        return "Route not defined"
        







