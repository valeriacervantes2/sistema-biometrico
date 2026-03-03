from app.database.database import get_connection

def insertar_rol(nombre, descripcion=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuario_rol (nombre, descripcion) VALUES (?, ?)", (nombre, descripcion))
    conn.commit()
    conn.close()

def obtener_roles():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuario_rol")
    datos = cursor.fetchall()
    conn.close()
    return datos

def actualizar_rol(id_rol, nombre=None, descripcion=None):
    conn = get_connection()
    cursor = conn.cursor()
    if nombre and descripcion:
        cursor.execute("UPDATE usuario_rol SET nombre = ?, descripcion = ? WHERE id_rol = ?", (nombre, descripcion, id_rol))
    elif nombre:
        cursor.execute("UPDATE usuario_rol SET nombre = ? WHERE id_rol = ?", (nombre, id_rol))
    elif descripcion:
        cursor.execute("UPDATE usuario_rol SET descripcion = ? WHERE id_rol = ?", (descripcion, id_rol))
    conn.commit()
    conn.close()

def desactivar_rol(id_rol):
    # opcional: si agregas campo estado
    pass