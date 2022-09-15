from flask import Flask, jsonify, request, make_response, render_template, session
import pymongo
import jwt
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt
import json
import codecs
from flask_jwt_extended import JWTManager
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
from bson.objectid import ObjectId
# import redis

app = Flask(__name__)
# configure_routes(app)

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

try:
    mongo = pymongo.MongoClient(
        host="localhost",
        port=27017,
        serverSelectionTimeoutMS=1000
    )
    db = mongo.userdata
except:
    print("Error: db not connected")

app.config['SECRET_KEY'] = '004f2af45d3a4e161a7dd2d17fdae47f'



@app.route("/register", methods=["POST"])
def register():

    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    pwd_hash = generate_password_hash(password)
    data = db.users.find_one({"email":email})
    if data:
        return jsonify({
        'message': "User exits with same email",
        'user': {
            'username': username, "email": email
        }
    })

    data = db.users.insert_one({"username":username, "email":email, "password":pwd_hash })
    
    return jsonify({
        'message': "User created",
        'user': {
            'username': username, "email": email
        }
    })


@app.route("/login", methods=['POST'])
def login():
    email = request.json.get('email', '')
    password = request.json.get('password', '')

    data = db.users.find_one({"email":email})
    if data:
        is_pass_correct = check_password_hash(data["password"], password)

        if is_pass_correct:
            refresh = create_refresh_token(identity=data["email"])
            access = create_access_token(identity=data["email"])

            return jsonify({
                'user': {
                    'refresh': refresh,
                    'access': access,
                    'username': data["username"],
                    'email': data["email"]
                }
            })
        
        else:
            return jsonify({
                'user': {'email': data["email"]},
                'error':"please check password"
            })
    
    return jsonify({'error': 'Wrong credentials'})



@app.route("/")
# @jwt_required()
def index():
    return "Hello, World!"


@app.route("/users", methods=["POST"])
# @jwt_required()
def create_user():
    data = json.loads(request.data)
    keys = ["name", "gender", "age", "email", "address"]
    for i in keys:
        if i not in data:
            raise KeyError("Required details must be present")
            
    name = request.json['name']
    gender = request.json['gender']
    age = request.json['age']
    email = request.json['email']
    address = request.json['address']

    data = db.user.insert_one({"name":name, "gender":gender, "age":age, 
    "email":email, "address":address})
    return jsonify({ "id":f"{data.inserted_id}" ,"name":name, "gender":gender, "age":age, 
    "email":email, "address":address})


@app.route("/alluser", methods=["GET"])
# @jwt_required()
def getallusers():
    users = list()
    data = db.user.find()
    for i in data:
        users.append({'id':f"{i['_id']}", 'name':i['name'], 'gender':i['gender'], 'age':i['age']})
    return jsonify(users)


@app.route("/delete/<id>", methods=["DELETE"])
def delete(id):
    db.user.delete_one({"_id":ObjectId(id)})
    return jsonify({
        "message":"user deleted succesfully",
    })


if __name__ == "__main__":
    app.run(debug=True)