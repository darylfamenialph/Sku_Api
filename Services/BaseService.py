import mysql.connector


def sku_connect():
    #my_db = mysql.connector.connect(host="10.0.0.6", user="chronos", passwd="#@$!MpL3_Bu+-C0mPl3x!", database="sku_api")
    my_db = mysql.connector.connect(host="localhost", user="root", passwd="password", database="sku_api")
    return my_db
