from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api
import format_csv
from pymongo import MongoClient
import os
from itsdangerous import (TimedJSONWebSignatureSerializer \
                                  as Serializer, BadSignature, \
                                  SignatureExpired)
from passlib.apps import custom_app_context as pwd_context

app = Flask(__name__)
api = Api(app)

client = MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'], 27017)
db1 = client.tododb

client = MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'], 27017)
db = client.userdb

SECRET_KEY = 'test1234@#$'

def generate_auth_token(id, expiration=600):
   # s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
   s = Serializer(SECRET_KEY, expires_in=expiration)
   # pass index of user
   return s.dumps({"id":id})

def verify_auth_token(token):
    s = Serializer(SECRET_KEY)
    try:
        data = s.loads(token)
    except SignatureExpired:
        app.logger.debug("***EXPIRED***")
        return None    # valid token, but expired
    except BadSignature:
        app.logger.debug("***BAD SIGNATURE***")
        return None    # invalid token
    return "Success"


class listAll(Resource):
    def get(self, dtype='json'):
        topk = request.args.get('top', default=-1, type=int)
        token = request.args.get('token', type=str)
        app.logger.debug(token)
        if token:
            if verify_auth_token(token):
                if dtype == 'csv':
                    return format_csv.csv_form(db1, topk), 201
                return make_response(format_csv.json_form(db1, topk),201)
        return make_response({'Failure':"Must be signed in to access resource"},401)

class listOpen(Resource):
    def get(self, dtype='json'):
        topk = request.args.get('top', default=-1, type=int)
        token = request.args.get('token', type=str)
        app.logger.debug(verify_auth_token(token))
        if token:
            if verify_auth_token(token):
                if dtype == 'csv':
                    return format_csv.csv_form(db1, topk, 'open'), 201
                return make_response(format_csv.json_form(db1, topk, 'open'),201)
        return make_response({'Failure':"Must be signed in to access resource"},401)

class listClose(Resource):
    def get(self, dtype='json'):
        topk = request.args.get('top', default=-1, type=int)
        token = request.args.get('token', type=str)
        if token:
            if verify_auth_token(token):
                if dtype == 'csv':
                    return format_csv.csv_form(db1, topk, 'close'), 201
                return make_response(format_csv.json_form(db1, topk, 'close'),201)
        return make_response({'Failure':"Must be signed in to access resource"},401)


class register(Resource):
    def post(self):
        password = request.args.get('password', type=str)
        username = request.args.get('username', type=str)
        entries = db.userdb.find()
        if not db.userdb.find_one({"username":username}):
            id = entries.count() + 1
            add = {'username': username, "password": pwd_context.encrypt(password), "id":id}
            db.userdb.insert_one(add)
            app.logger.debug("***SUCCESS***")
            app.logger.debug(add)
            return make_response(jsonify({'message':'Success'}), 201)
        return make_response(jsonify({'message':'Failure'}), 400)

class token(Resource):
    def get(self):
        password = request.args.get('password', type=str)
        username = request.args.get('username', type=str)
        dbUsername = db.userdb.find_one({'username':username})
        app.logger.debug(dbUsername)
        app.logger.debug(password)
        if dbUsername and pwd_context.verify(password, dbUsername['password']):
            app.logger.debug("***PASSWORDS MATCH***")
            response = {
                "response":"Success", 
                "id":dbUsername['id'],
                "token":str(generate_auth_token(dbUsername['id']))[2:-1]
                }
            app.logger.debug(f'***{dbUsername}')
            return response, 201
        return {'response':'Failure'}, 401

class _user1(Resource):
    def get(self):
        username = request.args.get('username')
        dbUsername = db.userdb.find_one({'username':username})
        if dbUsername:
            return jsonify(dbUsername)
        return jsonify({'username': "FAILURE"})

        

api.add_resource(listAll, '/listAll', '/listAll/<string:dtype>')
api.add_resource(listOpen, '/listOpenOnly', '/listOpenOnly/<string:dtype>')
api.add_resource(listClose, '/listCloseOnly', '/listCloseOnly/<string:dtype>')
api.add_resource(register, '/register')
api.add_resource(token, '/token')
api.add_resource(_user1, '/_user')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)