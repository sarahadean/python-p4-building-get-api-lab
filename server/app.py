#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

#returns array of json objects for all bakeries in the database
@app.route('/bakeries', methods = ["GET"])
def bakeries():
    #query and put into a variable
    bakery_list = Bakery.query.all()

    #serialize == changing format to dictionary form
    bakery_serialized = [bakery.to_dict() for bakery in bakery_list]
    
    #changing to JSON
    response = make_response(jsonify(bakery_serialized), 200)

    return response

#returns a single bakery as JSON with its baked goods nested in an array. 
# Use the id from the URL to look up the correct bakery.
@app.route('/bakeries/<int:id>', methods=["GET"])
def bakery_by_id(id):
    #query
    bakery = Bakery.query.filter(Bakery.id == id).first()
    #make dictionary - bakeries has already been serialized
    bakery_dict = bakery.to_dict()
   
    response = make_response(
        bakery_dict,
        200
    )
    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    #query
    baked_goods_pricing = BakedGood.query.order_by(BakedGood.price).all()
    #serialize
    serialized_goods = [goodies.to_dict() for goodies in baked_goods_pricing]
    #change to json
    response = make_response(
        jsonify(serialized_goods), 200)
    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    baked_goods_pricing = BakedGood.query.order_by(BakedGood.price.desc()).first()

    serialized_goods = baked_goods_pricing.to_dict()
    response = make_response(serialized_goods, 200)
    return response

if __name__ == '__main__':
    app.run(port=555, debug=True)
