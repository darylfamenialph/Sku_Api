from flask import Flask,jsonify, request
from flask_restful import Resource, Api
from Services import GetClient


app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        data = GetClient.get_client()
        return data

    def post(self):
        some_json = request.get_json()
        return {"you sent": some_json}, 201


class Multi(Resource):
    def get(self,num):
        return {"result": num*10}


api.add_resource(HelloWorld, '/')
api.add_resource(Multi, '/multi/<int:num>')


if __name__ == '__main__':
    app.run(debug=True)
