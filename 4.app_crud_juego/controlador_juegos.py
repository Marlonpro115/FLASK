from bd import obtener_conexion

def insertar_juego(nombre, descripcion, precio):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                "INSERT INTO juegos (nombre, descripcion, precio) VALUES (%s, %s, %s)",
                (nombre, descripcion, precio)
            )
        conexion.commit()
    except Exception as e:
        print(f"Error al insertar juego: {e}")
    finally:
        conexion.close()

def obtener_juegos():
    conexion = obtener_conexion()
    juegos = []
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id, nombre, descripcion, precio FROM juegos")
            juegos = cursor.fetchall()
    except Exception as e:
        print(f"Error al obtener juegos: {e}")
    finally:
        conexion.close()
    return juegos

def obtener_juego_por_id(id):
    conexion = obtener_conexion()
    juego = None
    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                "SELECT id, nombre, descripcion, precio FROM juegos WHERE id = %s", (id)
            )
            juego = cursor.fetchone()
    except Exception as e:
        print(f"Error al obtener juego por ID: {e}")
    finally:
        conexion.close()
    return juego

def actualizar_juego(nombre, descripcion, precio, id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                "UPDATE juegos SET nombre = %s, descripcion = %s, precio = %s WHERE id = %s",
                (nombre, descripcion, precio, id)
            )
        conexion.commit()
    except Exception as e:
        print(f"Error al actualizar juego: {e}")
    finally:
        conexion.close()

def eliminar_juego(id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM juegos WHERE id = %s", (id,))
        conexion.commit()
    except Exception as e:
        print(f"Error al eliminar juego: {e}")
    finally:
        conexion.close()