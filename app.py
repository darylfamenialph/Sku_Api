from flask import Flask,jsonify, request
from flask_restful import Resource, Api
from Logic import create_sku
import json


app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return "hello"

    def post(self):
        some_json = request.get_json()
        return {"you sent": some_json}, 201


class Multi(Resource):
    def get(self, num):
        return {"result": num*10}


class Get_SKU(Resource):
    def get(self, input_string):
        data = create_sku.generate_sku(input_string, 0)
        return data


class Generate_SKU(Resource):
    def post(self):
        request_json_data = json.dumps(request.get_json())
        parsed_json = json.loads(request_json_data)
        data = create_sku.generate_sku(parsed_json["input_string"], 0)
        return {"result": data}, 201


api.add_resource(HelloWorld, '/')
api.add_resource(Multi, '/multi/<int:num>')
api.add_resource(Get_SKU, '/get_sku/<string:input_string>')
api.add_resource(Generate_SKU, '/generate_sku')

if __name__ == '__main__':
    app.run(debug=True)
