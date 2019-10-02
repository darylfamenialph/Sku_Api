from Services import BaseService, GetClient, GetModel, GetCapacity
from mysql.connector import Error
from Logic import create_sku
import json

result = ""


class GetBlackBelt:
    def get_bb_code(manufacturer_name, model_name, capacity_value):
        try:

            if model_name.find(manufacturer_name) > -1:
                model_name = model_name.replace(manufacturer_name, "")

            connection = BaseService.sku_connect()
            cursor = connection.cursor()
            get_bb_qry = """SELECT
                                bb.bb_sku_code
                            FROM
                                blackbelt_sku bb
                                JOIN manufacturer manu ON manu.manufacturer_id = bb.manufacturer_id 
                                AND manu.is_active = 1
                                JOIN model m ON m.model_id = bb.model_id 
                                AND m.is_active = 1
                                JOIN capacity cap ON cap.capacity_id = bb.capacity_id
                                AND cap.is_active = 1
                            WHERE
                                manu.manufacturer_name = %s
                                AND m.model_name = %s
                                AND cap.capacity_value = %s
                                AND bb.void_record_id = 0;"""

            cursor.execute(get_bb_qry, (manufacturer_name, model_name, capacity_value))
            row_headers = [x[0] for x in cursor.description]
            data_collection = cursor.fetchall()

            data_array = []
            if len(data_collection) > 0:
                for data in data_collection:
                    data_array.append(dict(zip(row_headers, data)))
                result = json.dumps(data_array)
            else:
                client = GetClient.GetClient.get_client_code(manufacturer_name, 0)
                manu_json_data = json.loads(client)
                manufacturer_id = manu_json_data[0]["manufacturer_id"]
                manufacturer_code = manu_json_data[0]["manufacturer_code"]

                model = GetModel.GetModel.get_model_code(model_name, manufacturer_id, 0)
                model_json_data = json.loads(model)
                model_id = model_json_data[0]["model_id"]
                model_code = model_json_data[0]["model_code"]

                capacity = GetCapacity.GetCapacity.get_capacity_code(capacity_value)
                capacity_json_data = json.loads(capacity)
                capacity_id = capacity_json_data[0]["capacity_id"]
                capacity_value = capacity_json_data[0]["capacity_value"]

                data_code = manufacturer_code + model_code + str(capacity_value)
                insert_bb_sku = "INSERT INTO blackbelt_sku(manufacturer_id,model_id,capacity_id,bb_sku_code,bb_sku_description) VALUES(%s,%s,%s,%s,%s)"
                cursor.execute(insert_bb_sku, (manufacturer_id, model_id, capacity_id, data_code, "N/A"))
                connection.commit()

                return r'[{"bb_sku_code": "' + data_code + r'"}]'


        except Error as e:
            return e

        finally:
            if connection.is_connected():
                connection.close()
                cursor.close()

        return result



print(GetBlackBelt.get_bb_code("Huawei", "Huawei Mate 11 Pro", "256"))


