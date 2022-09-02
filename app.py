from email.policy import strict
from re import T
import re
from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
import json
from pathlib import Path
from flask_cors import CORS,cross_origin
## APP
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
cors = CORS(app)

ENV = 'production'

basedir = os.path.abspath(os.path.dirname(__file__)) 

if ENV == 'dev':
	app.debug = True
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'db.sqlite')
else:
	app.debug = False
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'db.sqlite')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init DB and MA
db =SQLAlchemy(app)
ma = Marshmallow(app)

@app.before_first_request
def check_db_data():
	filedb = "db.sqlite"
	path = Path(filedb)
	if path.is_file():
		pass
	else:
		db.create_all()
# Product Class/Model	
class Product(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(100),unique=True)
	description = db.Column(db.String(255))

	def __init__(self,name,description):
		self.name = name
		self.description = description

# Product Schema
class ProductSchema(ma.Schema):
	class Meta:
		fields = ('name','description','id')

# Init Schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# Create Product
@app.route('/product',methods=['POST'])
def add_product():
	name = request.json['name']
	description = request.json['description']

	new_product = Product(name,description)
	db.session.add(new_product)
	db.session.commit()

	return product_schema.jsonify(new_product)

# Get ALL Products
@app.route('/product',methods=['GET'])
def get_products():
	all_products = Product.query.all()
	results = products_schema.dump(all_products)
	return jsonify(results)

# Get One Product with ID
@app.route('/product/<id>',methods=['GET'])
def get_product(id):
	product = Product.query.get(id)
	return product_schema.jsonify(product)


# Update Product
@app.route('/product/<id>',methods=['PUT'])
def update_product(id):
	product = Product.query.get(id)
	name = request.json['name']
	description = request.json['description']

	product.name = name
	product.description = description

	db.session.commit()
	return product_schema.jsonify(product)


# Delete Product
@app.route('/product/<id>',methods=['DELETE'])
def delete_product(id):
	product = Product.query.get(id)
	db.session.delete(product)
	db.session.commit()
	return  jsonify({"Status":"OK"}) 
