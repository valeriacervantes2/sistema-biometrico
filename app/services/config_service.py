import os
import sqlite3

DB_PATH = os.path.join(os.getcwd(), "config_admin.db")

def inicializar_bd():
    """Crea la base de datos y la tabla de perfil si no existen, agregando un usuario administrador inicial."""
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS perfil_admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            a_paterno TEXT,
            a_materno TEXT,
            correo TEXT,
            telefono TEXT,
            facultad TEXT
        )
    """)
    
    # Comprobar si ya existe algún registro para no duplicar
    cursor.execute("SELECT COUNT(*) FROM perfil_admin")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO perfil_admin (nombre, a_paterno, a_materno, correo, telefono, facultad)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            "ADMINISTRADOR", 
            "DEL", 
            "SISTEMA", 
            "admin@universidad.edu.mx", 
            "5512345678", 
            "ADMINISTRACIÓN CENTRAL"
        ))
    conexion.commit()
    conexion.close()

def obtener_perfil():
    """Trae los datos de la fila del administrador."""
    inicializar_bd() # Asegura que la BD exista al intentar leer
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()
    cursor.execute("SELECT nombre, a_paterno, a_materno, correo, telefono, facultad FROM perfil_admin LIMIT 1")
    fila = cursor.fetchone()
    conexion.close()
    return fila

def actualizar_perfil(nombre, a_paterno, a_materno, correo, telefono):
    """Actualiza la información del perfil del administrador en la base de datos."""
    try:
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE perfil_admin
            SET nombre = ?, a_paterno = ?, a_materno = ?, correo = ?, telefono = ?
            WHERE id = (SELECT id FROM perfil_admin LIMIT 1)
        """, (nombre, a_paterno, a_materno, correo, telefono))
        conexion.commit()
        conexion.close()
        return True
    except Exception as e:
        print(f"Error al actualizar la base de datos: {e}")
        return False