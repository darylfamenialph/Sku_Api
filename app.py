from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from Services import GetClient, GetModel
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


class GenerateSku(Resource):
    def post(self):
        request_json_data = json.dumps(request.get_json())
        parsed_json = json.loads(request_json_data)
        client_data = json.dumps(GetClient.GetClient.get_client_code(parsed_json["Manufacturer"], 0))
        client_to_json = json.loads(client_data)
        model_data = GetModel.GetModel.get_model_code(parsed_json["Model"], client_to_json["manufacturer_id"], 0)
        model_to_json = json.loads(model_data)
        result_data = r'{"sku":"' + client_to_json["manufacturer_code"] + model_to_json["model_code"] + '"}'
        return {"result": result_data}, 201



api.add_resource(HelloWorld, '/')
api.add_resource(Multi, '/multi/<int:num>')
api.add_resource(Get_SKU, '/get_sku/<string:input_string>')
api.add_resource(GenerateSku, '/generate_make_sku')

if __name__ == '__main__':
    app.run(debug=True)
