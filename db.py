import pymysql

def create_connection():
    db = pymysql.connect("localhost", "root", "root", "shop")
    return db

