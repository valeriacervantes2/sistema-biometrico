from app.database.database import get_connection
from datetime import datetime

def insertar_usuario(nombre, a_paterno, a_materno, id_rol, id_facultad=None, id_carrera=None):
    conn = get_connection()
    cursor = conn.cursor()
    fecha = datetime.now().isoformat()
    cursor.execute("""
        INSERT INTO usuario (nombre, a_paterno, a_materno, fecha_registro, id_rol, id_facultad, id_carrera)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (nombre, a_paterno, a_materno, fecha, id_rol, id_facultad, id_carrera))
    conn.commit()
    conn.close()

def obtener_usuarios():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuario")
    datos = cursor.fetchall()
    conn.close()
    return datos

def actualizar_usuario(id_usuario, nombre=None, a_paterno=None, a_materno=None, id_rol=None):
    conn = get_connection()
    cursor = conn.cursor()
    fecha = datetime.now().isoformat()
    campos = []
    params = []

    if nombre:
        campos.append("nombre = ?")
        params.append(nombre)
    if a_paterno:
        campos.append("a_paterno = ?")
        params.append(a_paterno)
    if a_materno:
        campos.append("a_materno = ?")
        params.append(a_materno)
    if id_rol:
        campos.append("id_rol = ?")
        params.append(id_rol)

    campos.append("fecha_actualizacion = ?")
    params.append(fecha)

    query = "UPDATE usuario SET " + ", ".join(campos) + " WHERE id_usuario = ?"
    params.append(id_usuario)
    cursor.execute(query, tuple(params))
    conn.commit()
    conn.close()

def desactivar_usuario(id_usuario):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE usuario SET estado = 0, fecha_actualizacion = ? WHERE id_usuario = ?",
                    (datetime.now().isoformat(), id_usuario))
    conn.commit()
    conn.close()