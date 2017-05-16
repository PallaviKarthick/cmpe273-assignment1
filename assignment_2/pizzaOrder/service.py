import boto3
import json
from boto3 import dynamodb
from boto3.session import Session
import time

db_session = Session(aws_access_key_id='AKIAIXJMK3GZBLL4HM3Q' , aws_secret_access_key='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',region_name='us-west-1')
dynamodb = db_session.resource('dynamodb')
order_table = dynamodb.Table('Order')
menu_table = dynamodb.Table('Menu')
selection_map={}


def handler(event, context):
    method_type = event['httpMethod']
    if method_type=='POST':
        orderId=event['body']['order_id']
        customerName = event['body']['customer_name']
        order_table.put_item(
                                       Item = {
                                       "menu_id": event['body']['menu_id'],
                                       "order_id" :orderId,
                                       "customer_name" :customerName,
                                       "customer_email" :event['body']['customer_email']    
                                       })
        response = menu_table.get_item(
                                       Key={
                                       "menu_id":event['body']['menu_id']
                                       })
        selection=" "
        key=0
        for value in response['Item']['selection']:
            key+=1
            selection = selection + str(key) +"."+ value + " "
            selection_map[str(key)] = value
        response = "Hi " + customerName +" your order number is :"+orderId+" , please choose one of these selection: " + selection
        return json.dumps({'Message':response}, indent=4) 


    elif method_type=='GET' :
        response = order_table.get_item(
                                       Key={
                                       "order_id":event['body']['order_id']
                                       })
        return response['Item']

    elif method_type=='DELETE' :
        order_table.delete_item(
                               Key={
                               "order_id":event['body']['order_id']
                               })
        return "DELETED"

    elif method_type=='PUT' :
        selection_option = event['body']['input']
        print selection_option
        response_order = order_table.get_item(
                                       Key={
                                       "order_id":event['body']['order_id']
                                       })
        
        response_menu= menu_table.get_item(
                                       Key={
                                       "menu_id":response_order['Item']['menu_id']
                                       })
                                       
        
        selection=" "
        key=0
        for value in response_menu['Item']['selection']:
            key+=1
            selection = selection + str(key) +"."+ value + " "
            selection_map[str(key)] = value
        selection = selection_map[selection_option]

        size=" "
        key=0
        for value in response_menu['Item']['size']:
            key+=1
            size = size + str(key) +"."+ value + " "
        print size
        order_table.update_item(
                                        Key={
                                        "order_id":event['body']['order_id']},
                                        UpdateExpression ='SET order_details = :or',
                                        ExpressionAttributeValues = { ':or' : {'selection' : selection  }}
                                        )
      
        #print size
        response = "Which size do you want?" + size
        return json.dumps({'Message':response}, indent=4) 
    else :
        return "Route not defined" 





