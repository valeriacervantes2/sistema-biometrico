import sqlite3
import os

BASE_DIR = os.getcwd()
DB_PATH = os.path.join(BASE_DIR, "configuracion_admin.db")

def inicializar_bd_configuracion():
    """Crea el archivo de base de datos y la tabla si no existen."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
   
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
    

    cursor.execute("SELECT COUNT(*) FROM perfil_admin")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO perfil_admin (nombre, a_paterno, a_materno, correo, telefono, facultad)
            VALUES ('ADMINISTRADOR', 'DEL SISTEMA', '', 'admin@universidad.edu.mx', '5512345678', 'ADMINISTRACIÓN CENTRAL')
        """)
        conn.commit()
        
    conn.close()

def obtener_perfil():
    """Obtiene los datos del perfil para mostrarlos en la pantalla."""
    inicializar_bd_configuracion()  
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, a_paterno, a_materno, correo, telefono, facultad FROM perfil_admin WHERE id = 1")
    datos = cursor.fetchone()
    conn.close()
    return datos

def actualizar_perfil(nombre, a_paterno, a_materno, correo, telefono):
    """Guarda los nuevos datos que el usuario escribió en las cajas de texto."""
    conn = sqlite3.connect(DB_PATH)
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE perfil_admin 
            SET nombre = ?, a_paterno = ?, a_materno = ?, correo = ?, telefono = ? 
            WHERE id = 1
        """, (nombre, a_paterno, a_materno, correo, telefono))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error al actualizar configuración: {e}")
        return False
    finally:
        conn.close()