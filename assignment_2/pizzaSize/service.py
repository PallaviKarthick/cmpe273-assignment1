import boto3
import json
from boto3 import dynamodb
import uuid
from boto3.session import Session
import time

db_session = Session(aws_access_key_id='AKIAIXJMK3GZBLL4HM3Q' , aws_secret_access_key='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',region_name='us-west-1')
dynamodb = db_session.resource('dynamodb')
order_table = dynamodb.Table('Order')
menu_table = dynamodb.Table('Menu')
selection_map={}


def handler(event, context):
    method_type = event['httpMethod']

    if method_type=='PUT' :
        size_option = event['body']['input']
        print size_option
        response_order = order_table.get_item(
                                       Key={
                                       "order_id":event['body']['order_id']
                                       })
        
        response_menu= menu_table.get_item(
                                       Key={
                                       "menu_id":response_order['Item']['menu_id']
                                       })
                                       
        
        selection= response_order['Item']['order_details']['selection']
        size = response_menu['Item']['size'][int(size_option)-1]
        price = response_menu['Item']['price'][int(size_option)-1]
        print selection
        print size
        print price
        order_table.update_item(
                                        Key={
                                        "order_id":event['body']['order_id']},
                                        UpdateExpression ='SET order_details = :or , order_status = :os',
                                        ExpressionAttributeValues = { ':or' : {'selection' : selection ,'size' : size , 'costs':price , 'order_time': time.strftime("%m-%d-%Y@%H:%M:%S") },
                               ':os' : "Processing"
                                }
        )
        response = "Your order costs $"+ price +". We will email you when the order is ready. Thank you!"
        return json.dumps({'Message':response}, indent=4) 
    else :
        return "Route not defined" 





