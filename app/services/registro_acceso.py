from app.database.database import get_connection
from datetime import datetime


# ==========================
# REGISTRAR ACCESO
# ==========================

def registrar_acceso(id_usuario, resultado, confianza=None, motivo=None):
    conn = get_connection()
    cursor = conn.cursor()

    fecha = datetime.now().isoformat()

    cursor.execute("""
        INSERT INTO registro_acceso (
            id_usuario,
            fecha_hora,
            resultado,
            confianza,
            motivo
        ) VALUES (?, ?, ?, ?, ?)
    """, (id_usuario, fecha, resultado, confianza, motivo))

    conn.commit()
    conn.close()


# ==========================
# OBTENER HISTORIAL POR USUARIO
# ==========================

def obtener_historial_usuario(id_usuario):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM registro_acceso
        WHERE id_usuario = ?
        ORDER BY fecha_hora DESC
    """, (id_usuario,))

    datos = cursor.fetchall()
    conn.close()
    return datos


# ==========================
# OBTENER INTENTOS FALLIDOS
# ==========================

def obtener_intentos_fallidos():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM registro_acceso
        WHERE resultado = 0
        ORDER BY fecha_hora DESC
    """)

    datos = cursor.fetchall()
    conn.close()
    return datos