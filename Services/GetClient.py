from Services import BaseService
from mysql.connector import Error
from Logic import create_sku
import json

result = ""


class GetClient:
    def get_client_code(client_string, iteration):
        try:
            connection = BaseService.sku_connect()
            cursor = connection.cursor()
            get_client_qry = "SELECT manufacturer_id,manufacturer_name, manufacturer_code,iteration FROM manufacturer WHERE is_active = 1 AND manufacturer_name= %s;"

            cursor.execute(get_client_qry, (client_string,))

            data_collection = cursor.fetchall()
            data_array = []
            if len(data_collection) > 0:
                for data in data_collection:
                    data_array.append({r'manufacturer_id': data[0], r'manufacturer_name': data[1], r'manufacturer_code': data[2], r'iteration': data[3]})
                result = json.dumps(data_array)
            else:
                generated_sku = create_sku.generate_sku(client_string, iteration)
                check_client = "SELECT manufacturer_id,manufacturer_name, manufacturer_code,iteration FROM manufacturer WHERE is_active = 1 AND manufacturer_code= %s;"
                cursor.execute(check_client, (generated_sku,))
                check_result = cursor.fetchall()
                client_iteration = 0
                for row in check_result:
                    if len(row) > 0:
                        client_iteration = int(row[3])
                    else:
                        client_iteration = 0

                iteration = client_iteration + 1

                existence_result = 1
                while existence_result > 0:
                    next_iteration_generated_sku = create_sku.generate_sku(client_string, iteration)
                    check_client_code_existence = "SELECT COUNT(*) FROM manufacturer WHERE is_active = 1 AND manufacturer_code= %s;"
                    cursor.execute(check_client_code_existence, (next_iteration_generated_sku,))
                    check_existence_result = cursor.fetchone()
                    existence_result = int(check_existence_result[0])
                    if existence_result > 0:
                        iteration += 1

                insert_client = "INSERT INTO manufacturer(manufacturer_name,manufacturer_code,iteration) VALUES(%s,%s,%s)"
                cursor.execute(insert_client, (client_string, next_iteration_generated_sku,iteration))
                connection.commit()
                # Getting Inserted Data
                check_new_inserted_client = "SELECT manufacturer_id,manufacturer_name, manufacturer_code,iteration FROM manufacturer WHERE is_active = 1 AND manufacturer_code= %s;"
                cursor.execute(check_new_inserted_client, (next_iteration_generated_sku,))
                check_new_result = cursor.fetchall()
                new_result_array = []
                for new_result in check_new_result:
                    new_result_array.append({r'manufacturer_id': new_result[0], r'manufacturer_name': new_result[1], r'manufacturer_code': new_result[2], r'iteration': new_result[3]})
                result = json.dumps(new_result_array)


        except Error as e:
            return e

        finally:
            if (connection.is_connected()):
                connection.close()
                cursor.close()

        return result


print(GetClient.get_client_code("Appleseed", 0))


