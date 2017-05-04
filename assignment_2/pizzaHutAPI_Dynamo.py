from __future__ import print_function 
from flask import Flask, request
from github import Github
import sys
from flask import Flask,jsonify
import re
from Menu import Menu
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import uuid


dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
table = dynamodb.Table('Menu')

table_Order = dynamodb.Table('Order')



app = Flask(__name__)


'''  Pizza Menu CRUD APIs'''

@app.route("/", methods=['GET'])
def hello():
    return jsonify({
        'author': 'Pallavi Jakanachary',
        'application': 'PizzaHut API'
    })


@app.route("/menu", methods=['POST'])
def newMenu():
    req = request.get_json(force=True)
    if request.method == 'POST':
        ##print req
        menu = Menu(req['store_name'])
        menu.price['price'] = req['price']
        menu.selection['selection'] = req['selection']
        menu.size['size'] = req['size']
        menu.store_hours['store_hours'] = req['store_hours']
        menu.status='CREATED'
        menu.message='Menu created'
        table.put_item(Item={
            'menu_id' :menu.menu_id,
            'store_name':menu.store_name,
            'selection':menu.selection['selection'],
            'size':menu.size['size'],
            'prize':menu.price['price'],
            'store_hours':menu.store_hours['store_hours']
        })
        print ("Menu created !!")
    response = jsonify({'status':'Menu created'}) 
    response.status_code=200
    return response



@app.route("/menu/<string:menuId>", methods=['GET'])
def viewMenu(menuId):
    try:
        response = table.get_item(Key={
            'menu_id': menuId
         })
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        item = response['Item']
    print("Get Menu succeeded:")
    print(json.dumps(item, indent=4)) 
    return jsonify(item)


@app.route("/menu/<string:menuId>",methods=['DELETE'])
def deleteMenu(menuId):
    if request.method == 'DELETE':
        print (menuId)
        response = table.delete_item(Key={
            'menu_id': menuId
        })
        response = jsonify({})
        response.status_code = 200
        return response

@app.route("/menu/<string:menuId>", methods=['PUT'])
def updateMenu(menuId):
    req = request.get_json(force=True)
    print(req['selection'])
    response = table.update_item(Key={
    'menu_id': menuId
    },
    UpdateExpression="set selection = :s",
    ExpressionAttributeValues={
        ':s': req['selection']
    },
    ReturnValues="UPDATED_NEW"
    )
    print("Update Menu succeeded:")
    print(json.dumps(response, indent=4))
    if response:
        try:
            response = table.get_item(Key={
            'menu_id': menuId
         })
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            item = response['Item']
        print("Get Menu succeeded:")
        print(json.dumps(item, indent=4)) 
        return jsonify(item)
          

'''  Pizza Order Processing APIs'''

@app.route("/order", methods=['POST'])
def newOrder():
    req = request.get_json(force=True)
    message=""
    if request.method == 'POST':
        ##print req
        order_id = str(uuid.uuid4())
        customer_name = req['customer_name']
        customer_email = req['customer_email']
        # table.put_item(Item={
        #     'order_id' :order_id,
        #     'customer_name':customer_name,
        #     'customer_email':customer_email
        # })
        print ("Order created !!")
        message = "Hi "+ customer_name +", please choose one of these selection:  1. Cheese, 2. Pepperoni, 3.Vegetable"
    response = jsonify({'Message':message}) 
    response.status_code=200
    return response


                        
if __name__ == "__main__":
    app.run(debug = True, host = '0.0.0.0', port = 8080)