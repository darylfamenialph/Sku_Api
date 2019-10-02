from Services import BaseService
from mysql.connector import Error
from Logic import create_sku
import json

result = ""


class GetCapacity:
    def get_capacity_code(capacity_value):
        try:
            check_capacity = capacity_value.find(".0 GB")
            if check_capacity > -1:
                capacity_value = capacity_value.replace(".0 GB", "")

            connection = BaseService.sku_connect()
            cursor = connection.cursor()
            get_capacity_qry = "SELECT capacity_id, capacity_value FROM capacity cap WHERE cap.is_active = 1 AND cap.capacity_value = %s"

            cursor.execute(get_capacity_qry, (int(capacity_value),))
            row_headers = [x[0] for x in cursor.description]
            data_collection = cursor.fetchall()

            data_array = []
            if len(data_collection) > 0:
                for data in data_collection:
                    data_array.append(dict(zip(row_headers, data)))
                result = json.dumps(data_array)
            else:

                insert_capacity = "INSERT INTO capacity(capacity_value,capacity_uom) VALUES(%s,%s)"
                cursor.execute(insert_capacity, (int(capacity_value), "GB"))
                connection.commit()
                # Getting Inserted Data
                check_new_inserted_capacity = "SELECT capacity_id, capacity_value FROM capacity cap WHERE cap.is_active = 1 AND cap.capacity_value = %s"
                cursor.execute(check_new_inserted_capacity, (int(capacity_value),))
                new_row_headers = [x[0] for x in cursor.description]
                check_new_result = cursor.fetchall()
                new_result_array = []
                for new_result in check_new_result:
                    new_result_array.append(dict(zip(new_row_headers, new_result)))
                result = json.dumps(new_result_array)


        except Error as e:
            return e

        finally:
            if connection.is_connected():
                connection.close()
                cursor.close()

        return result


#print(GetCapacity.get_capacity_code("257.0 GB"))


