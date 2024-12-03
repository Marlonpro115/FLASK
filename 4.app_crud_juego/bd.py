import pymysql
from pymysql import MySQLError

def obtener_conexion():
    try:
        conexion = pymysql.connect(
            host='localhost',
            user='root',
            passwd='',
            db='app_crud_juego',
            cursorclass=pymysql.cursors.DictCursor
        )
        return conexion
    except MySQLError as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None