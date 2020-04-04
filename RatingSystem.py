from flask import Flask, render_template, request, jsonify, redirect, session
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask import abort
from flask_cors import CORS, cross_origin
from flask import make_response, url_for
import json
from time import gmtime, strftime
import random
from pymongo import MongoClient
from time import gmtime, strftime
import sqlite3
import os
from werkzeug.datastructures import FileStorage


#Connection to MongoDB Database
connection = MongoClient("mongodb://localhost:27017/")

UPLOAD_FOLDER = '/static/img'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
# Object creation
app = Flask(__name__)




app.config.from_object(__name__)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'
CORS(app)
photos = UploadSet('photos', IMAGES)
configure_uploads(app, (photos,))

app = Flask(__name__) 


def create_mongodatabase():
    try:
        dbnames = connection.database_names()
        if 'ccc_cloud_native' not in dbnames:
            db = connection.ccc_cloud_native.users
            db_products = connection.ccc_cloud_native.db_products
            db_reviews = connection.ccc_cloud_native.db_reviews
            db_api = connection.ccc_cloud_native.apirelease

            db.insert({
                "email": "lee@google.com",
                "id": 33,
                "name": "Lee Ellis",
                "password": "ass_word"
                })

            db_products.insert({
                "name": "Blender",
                "id": 18,
                "timestamp": "2017-93-11T06:39:40Z",
                "price": "£30.99",
                "image": "/images/blender1.jpg",
                "category": "catering",
                "description": "A blender, which blends stuff basically"
                })

            db_reviews.insert({
                "body": "Great blender, use it all the time",
                "product_id": 18,
                "id": 1,
                "timestamp": "2017-93-11T06:39:40Z",
                "postedby": "Lee Ellis",
                "rating": 3
                })

            db_api.insert( {
                "buildtime": "2020-03-16 13:00:00",
                "links": "/api/v1/api_users",
                "methods": "get, post, put , delete",
                "version": "v1"
                })
            db_api.insert( {
                "buildtime": "2020-03-16 13:00:00",
                "links": "/api/v2/api_products",
                "methods": "get, post",
                "version": "v2"
                })
            db_api.insert( {
                "buildtime": "2020-03-16 13:00:00",
                "links": "/api/v3/api_reviews",
                "methods": "get, post, put",
                "version": "v3"
                })
            print ("Database Initialize completed!")
        else:
            print ("Database already Initialized!")
    except:
        print ("Database creation failed!!")
#Users
def list_users():
    api_list=[]
    db = connection.ccc_cloud_native.users
    for row in db.find({}, {'_id':0}):
        api_list.append(row)
    # print (api_list)
    return jsonify({'user_list': api_list})
#List specific users
def list_user(user_id):
    print (user_id);
    api_list=[]
    db = connection.ccc_cloud_native.users
    for i in db.find({'id':user_id}):
        api_list.append(str(i))
    if api_list == []:
        abort(404)
    return jsonify({'user_details':api_list})

def add_user(new_user): 
    api_list=[] 
    print (new_user) 
    db = connection.ccc_cloud_native.users 
    user = db.find({'$or':[{"name":new_user['name']} ,{"email":new_user['email']}]}) 
    for i in user: 
       print (str(i)) 
       api_list.append(str(i)) 
#print (api_list)
    if api_list == []: 
#print(new_user)
       db.insert(new_user) 
       return "Success" 
    else : 
       abort(409) 

def upd_user(user): 
    api_list=[] 
    print (user) 
    db_user = connection.ccc_cloud_native.users 
    users = db_user.find_one({"id":user['id']}) 
    for i in users: 
        api_list.append(str(i)) 
    if api_list == []: 
        abort(409) 
    else: 
        db_user.update({'id':user['id']},{'$set': user}, upsert=False ) 
        return "Success" 

def del_user(del_user): 
    db = connection.ccc_cloud_native.users 
    api_list = [] 
    for i in db.find({'name':del_user}): 
        api_list.append(str(i)) 
 
    if api_list == []: 
        abort(404) 
    else: 
        db.remove({"name":del_user}) 
        return "Success" 
#Products
def list_products():
    api_list=[]
    db = connection.ccc_cloud_native.db_products
    for row in db.find({}, {'_id':0}):
        api_list.append(row)
    #print (api_list)
    return jsonify({'product_list': api_list})

def list_product(user_id):
    print (user_id)
    db = connection.ccc_cloud_native.db_products
    api_list=[]
    product = db.find({'id':product_id})
    for i in product:
        api_list.append(str(i))
    if api_list == []:
        abort(404)
    return jsonify({'product': api_list})

def add_product(new_product):
    api_list=[]
    print (new_product)
    db_product = connection.ccc_cloud_native.db_products
    for i in new_product:
        api_list.append(str(i))
    if api_list == []:
        abort(404)
    else:
       db_product.insert(new_product)
       return "Success"

def upd_product(product): 
    api_list=[] 
    print (product) 
    db_product = connection.ccc_cloud_native.db_products 
    products = db_product.find_one({"id":product['id']}) 
    for i in product: 
        api_list.append(str(i)) 
    if api_list == []: 
        abort(409) 
    else: 
        db_product.update({'id':product['id']},{'$set': product}, upsert=False ) 
        return "Success" 

def del_product(del_product): 
    db = connection.ccc_cloud_native.db_products 
    api_list = [] 
    for i in db.find({'name':del_product}): 
        api_list.append(str(i)) 
 
    if api_list == []: 
        abort(404) 
    else: 
        db.remove({"name":del_product}) 
        return "Success" 

def list_reviews():
    api_list=[]
    db = connection.ccc_cloud_native.db_reviews
    for row in db.find():
        api_list.append(str(row))
    #print (api_list)
    return jsonify({'review_list': api_list})

def list_review(review_id):
    print (review_id)
    db = connection.ccc_cloud_native.db_reviews
    api_list=[]
    review = db.find({'id':review_id})
    for i in review:
        api_list.append(str(i))
    if api_list == []:
        abort(404)
    return jsonify({'review': api_list})

def add_review(new_review):
    api_list=[]
    print (new_review)
    db_review = connection.ccc_cloud_native.db_reviews
    for i in new_review:
        api_list.append(str(i))
    if api_list == []:
        abort(404)
    else:
       db_review.insert(new_review)
       return "Success"

def upd_review(review):  #Not working: PUT request rtns success but no update to the db
    api_list=[] 
    print (review) 
    db_review = connection.ccc_cloud_native.db_reviews 
    review = db_review.find_one({"id":review['id']}) 
    for i in review: 
        api_list.append(str(i)) 
    if api_list == []: 
        abort(409) 
    else: 
        db_review.update({'id':review['id']},{'$set': review}, upsert=False ) 
        return "Success" 

def del_review(del_review): 
    db = connection.ccc_cloud_native.db_reviews 
    api_list = [] 
    for i in db.find({'id':del_review}): 
        api_list.append(str(i)) 
 
    if api_list == []: 
        abort(404) 
    else: 
        db.remove({"id":del_review}) 
        return "Success" 

@app.route("/api/v1/api_info")
def home_index():
    api_list=[]
    db = connection.ccc_cloud_native.apirelease
    for row in db.find():
        api_list.append(str(row))
    return jsonify({'api_version': api_list}), 200

@app.route('/api/v1/users', methods=['GET'])
def get_users():
    return list_users()
@app.route('/api/v1/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return list_user(user_id)
@app.route('/api/v1/users', methods=['POST'])
def create_user(): 
    if not request.json or not 'email' in request.json or not 'name' in request.json: 
        abort(400) 
    user = { 
        'email': request.json['email'], 
        'id': random.randint(1,1000),
        'name': request.json.get('name',"")
        
    } 
    return jsonify({'status': add_user(user)}), 201

@app.route('/api/v1/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = {}
    # if not request.json:
    #     abort(400)
    user['id']=user_id
    key_list = request.json.keys()
    for i in key_list:
        user[i] = request.json[i]
    print (user)

    return jsonify({'status': upd_user(user)}), 200

@app.route('/api/v1/users', methods=['DELETE'])
def delete_user():
    if not request.json or not 'name' in request.json:
        abort(400)
    user=request.json['name']
    return jsonify({'status': del_user(user)}), 200

@app.route('/api/v2/products', methods=['GET'])
def get_products():
    return list_products()
@app.route('/api/v2/products/<int:id>', methods=['GET'])
def get_product(id):
    return list_product(id)
@app.route('/upload', methods=['POST'])
def upload():
    if 'image' in request.files:
        file = request.files['image']
        file.save(os.path.join("static/img", file.filename))
        return render_template('addproducts.html', message=file.filename)
@app.route('/api/v2/products', methods=['POST'])
def add_products():
    product = {}  
    if not request.json or not 'name' in request.json or not 'category' in request.json or not 'price' in request.json or not 'description' in request.json:
        abort(400)
    product['name'] = request.json['name']
    product['category'] = request.json['category']
    product['id'] = random.randint(1,1000)
    product['price'] = request.json['price']
    product['description'] = request.json['description']
    product['image'] = request.json['image'].replace("C:\\fakepath\\", "static\\img\\")
    product['timestamp'] = strftime("%Y-%m-%dT%H:%M:%SZ", gmtime())
    print (product)
    return  jsonify({'status': add_product(product)}), 201

@app.route('/api/v2/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = {}
    # if not request.json:
    #     abort(400)
    product['id']=product_id
    key_list = request.json.keys()
    for i in key_list:
        product[i] = request.json[i]
    print (product)

    return jsonify({'status': upd_product(product)}), 200

@app.route('/api/v2/products', methods=['DELETE'])
def delete_product():
    if not request.json or not 'name' in request.json:
        abort(400)
    product=request.json['name']
    return jsonify({'status': del_product(product)}), 200

#Reviews
@app.route('/api/v3/reviews', methods=['GET'])
def get_reviews():
    return list_reviews()
@app.route('/api/v3/reviews/<int:id>', methods=['GET'])
def get_review(id):
    return list_review(id)
@app.route('/api/v3/reviews', methods=['POST'])
def add_reviews():

    review = {}
    if not 'body' in request.json or not 'rating' in request.json:
        abort(400)
    review['body'] = request.json['body']
    review['id'] = random.randint(1,1000)
    review['product_id'] = request.json['product_id']
    review['timestamp']=strftime("%Y-%m-%dT%H:%M:%SZ", gmtime())
    review['createdby'] = request.json['createdby']
    review['rating'] = request.json['rating']
     
    print (review)
    return  jsonify({'status': add_review(review)}), 201

@app.route('/api/v3/reviews/<int:review_id>', methods=['PUT'])
def update_review(review_id):
    review = {}
    # if not request.json:
    #     abort(400)
    review['id']=review_id
    key_list = request.json.keys()
    for i in key_list:
        review[i] = request.json[i]
    print (review)

    return jsonify({'status': upd_review(review)}), 200

@app.route('/api/v3/reviews', methods=['DELETE'])
def delete_review():
    if not request.json or not 'id' in request.json: #select the values to test here, perhaps "createdby"
        abort(400)
    review=request.json['id']
    return jsonify({'status': del_review(review)}), 200

#Views/Templates
@app.route('/adduser')
def adduser():
    return render_template('adduser.html')
@app.route('/addproducts')
def showproducts():
    return render_template('addproducts.html')
@app.route('/reviewproducts.htmls')

@app.errorhandler(404)
def resource_not_found(error):
    return make_response(jsonify({'error': 'Resource not found!'}), 404)

@app.errorhandler(409)
def user_found(error):
    return make_response(jsonify({'error': 'Conflict! Record exist'}), 409)

@app.errorhandler(400)
def invalid_request(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)

if __name__ == "__main__": 
	create_mongodatabase()
	app.run(host='0.0.0.0', port=5000, debug=True) 

