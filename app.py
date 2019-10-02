from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from Services import GetBlackbeltCode
from Logic import create_sku
import json
import os


app = Flask(__name__)
api = Api(app)



class GenerateSku(Resource):
    def post(self):
        try:
            request_json_data = json.dumps(request.get_json())
            parsed_json = json.loads(request_json_data)
            access_token = parsed_json["access_token"]
            if access_token == "x89dREsfoiuwai8Rxfaoi902UEyRi9S":
                data = GetBlackbeltCode.GetBlackBelt.get_bb_code(parsed_json["Manufacturer"], parsed_json["Model"], str(parsed_json["Capacity"]))
            else:
                data = r'[{"result":"Access Token is not valid"}]'
            return data
        except:
            return r'[{"result":"Missing Parameters"}]'



api.add_resource(GenerateSku, '/generate_sku')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 9234))
    app.run(debug=True, host='127.0.0.1', port=port)
