from flask import Flask ,request
from github import Github
import sys
from flask import Flask,jsonify
import re
from Menu import Menu
from pymongo import MongoClient


client =MongoClient('localhost', 27017)
db = client['pizzaHut']
collection = db['menu']



app = Flask(__name__)

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
        menu.price['price'] = (req['price'])
        menu.selection['selection'] = (req['selection'])
        menu.size['size'] = (req['size'])
        menu.store_hours['store_hours'] = (req['store_hours'])
        menu.status='CREATED'
        menu.message='Menu created'
        menu_db = {
            'menu_id' :menu.menu_id,
            'store_name':menu.store_name,
            'selection':menu.selection['selection'],
            'size':menu.size['size'],
            'prize':menu.price['price'],
            'store_hours':menu.store_hours['store_hours']
        }
        insertdb = collection.insert_one(menu_db).inserted_id
        print insertdb   
    response = jsonify({'status':'Menu created'}) 
    response.status_code=200
    return response



@app.route("/v1/<string:fileName>", methods=['GET'])
def v1(fileName):
    return "pallavi"
                        
if __name__ == "__main__":
    app.run(debug = True, host = '0.0.0.0', port = 8080)