from Services import BaseService
from mysql.connector import Error
from Logic import create_sku




class GetModel:
    def get_model_code(model_string, manufacturer_id, iteration):
        try:
            result = ""
            connection = BaseService.sku_connect()
            cursor = connection.cursor()
            get_model_qry = "SELECT manufacturer_id,model_id,model_name, model_code,iteration FROM model WHERE is_active = 1 AND manufacturer_id= %s AND model_name= %s;"

            cursor.execute(get_model_qry, (manufacturer_id, model_string,))

            data = cursor.fetchall()
            if len(data) > 0:
                result = data
            else:
                generated_sku = create_sku.generate_sku(model_string, iteration)
                check_model = "SELECT manufacturer_id,model_id,model_name, model_code,iteration FROM model WHERE is_active = 1 AND manufacturer_id= %s AND model_code= %s;"
                cursor.execute(check_model, (manufacturer_id, generated_sku,))
                check_result = cursor.fetchall()
                for row in check_result:
                    model_iteration = int(row[4])

                if len(check_result) > 0:

                    iteration = model_iteration + 1

                    existence_result = 1
                    while existence_result > 0:
                        next_iteration_generated_sku = create_sku.generate_sku(model_string, iteration)
                        check_model_code_existence = "SELECT COUNT(*) FROM model WHERE is_active = 1 AND manufacturer_id= %s AND model_code= %s;"
                        cursor.execute(check_model_code_existence, (manufacturer_id, next_iteration_generated_sku,))
                        check_existence_result = cursor.fetchone()
                        existence_result = int(check_existence_result[0])
                        if existence_result > 0:
                            iteration += 1

                    insert_model = "INSERT INTO model(manufacturer_id,model_name,model_code,iteration) VALUES(%s,%s,%s,%s)"
                    cursor.execute(insert_model, (manufacturer_id, model_string, next_iteration_generated_sku, iteration))
                    connection.commit()
                    # Getting Inserted Data
                    check_new_inserted_model = "SELECT manufacturer_id,model_id,model_name, model_code,iteration FROM model WHERE is_active = 1 AND manufacturer_id = %s AND model_code= %s;"
                    cursor.execute(check_new_inserted_model, (manufacturer_id, next_iteration_generated_sku,))
                    check_new_result = cursor.fetchall()

                    result = check_new_result

                else:
                    result = check_result

        except Error as e:
            return e

        finally:
            if (connection.is_connected()):
                connection.close()
                cursor.close()

        return result


print(GetModel.get_model_code("iPhone 7", 2, 0))


