from Services import BaseService
from mysql.connector import Error
from Logic import create_sku

result = ""


class GetClient:
    def get_client_code(client_string, iteration):
        try:
            connection = BaseService.sku_connect()
            cursor = connection.cursor()
            get_client_qry = "SELECT manufacturer_id,manufacturer_name, manufacturer_code,iteration FROM manufacturer WHERE is_active = 1 AND manufacturer_name= %s;"

            cursor.execute(get_client_qry, (client_string,))

            data = cursor.fetchall()
            if len(data) > 0:
                result = data
            else:
                generated_sku = create_sku.generate_sku(client_string, iteration)
                check_client = "SELECT manufacturer_id,manufacturer_name, manufacturer_code,iteration FROM manufacturer WHERE is_active = 1 AND manufacturer_code= %s;"
                cursor.execute(check_client, (generated_sku,))
                check_result = cursor.fetchall()
                for row in check_result:
                    client_iteration = int(row[3])

                if len(check_result) > 0:
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


print(GetClient.get_client_code("Applesfariuusr", 0))


