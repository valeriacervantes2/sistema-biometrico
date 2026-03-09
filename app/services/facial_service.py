import sqlite3
import numpy as np
from datetime import datetime
from database import get_connection

#-------------
# ==============================
# CREAR USUARIO
# ==============================

def crear_usuario(nombre, a_paterno, a_materno, id_rol,
                id_facultad=None, id_carrera=None):
    conn = get_connection()
    cursor = conn.cursor()

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO usuario (
            nombre, a_paterno, a_materno,
            estado, fecha_registro,
            id_rol, id_facultad, id_carrera
        ) VALUES (?, ?, ?, 1, ?, ?, ?, ?)
    """, (nombre, a_paterno, a_materno,
          fecha, id_rol, id_facultad, id_carrera))

    usuario_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return usuario_id


# ==============================
# GUARDAR EMBEDDING
# ==============================

def guardar_embedding(id_usuario, encoding_numpy):
    """
    encoding_numpy debe ser un vector numpy (128 valores)
    generado por face_recognition
    """

    conn = get_connection()
    cursor = conn.cursor()

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Convertimos numpy array a BLOB
    embedding_blob = encoding_numpy.tobytes()

    cursor.execute("""
        INSERT INTO biometria (
            id_usuario, embedding,
            fecha_registro, estado
        ) VALUES (?, ?, ?, 1)
    """, (id_usuario, embedding_blob, fecha))

    conn.commit()
    conn.close()


# ==============================
# OBTENER EMBEDDINGS ACTIVOS
# ==============================

def obtener_embeddings_activos():
    """
    Devuelve:
    - lista de encodings numpy
    - lista de ids_usuario correspondientes
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id_usuario, embedding
        FROM biometria
        WHERE estado = 1
    """)

    registros = cursor.fetchall()
    conn.close()

    lista_ids = []
    lista_embeddings = []

    for id_usuario, embedding_blob in registros:
        encoding = np.frombuffer(embedding_blob, dtype=np.float64)
        lista_ids.append(id_usuario)
        lista_embeddings.append(encoding)

    return lista_ids, lista_embeddings


# ==============================
# REGISTRAR ACCESO
# ==============================

def registrar_acceso(id_usuario, resultado, confianza,
                    motivo=None):
    """
    resultado:
        1 = permitido
        0 = denegado
    motivo:
        baja_confianza
        no_reconocido
        liveness_fallido
        usuario_inactivo
    """

    conn = get_connection()
    cursor = conn.cursor()

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO registro_acceso (
            id_usuario, fecha_hora,
            resultado, confianza, motivo
        ) VALUES (?, ?, ?, ?, ?)
    """, (id_usuario, fecha,
        resultado, confianza, motivo))

    conn.commit()
    conn.close()


# ==============================
# OBTENER CONFIGURACIÓN
# ==============================

def obtener_configuracion():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT tolerance, liveness_activo
        FROM configuracion_sistema
        LIMIT 1
    """)

    config = cursor.fetchone()
    conn.close()

    if config:
        return {
            "tolerance": config[0],
            "liveness_activo": config[1]
        }
    else:
        # valores por defecto si algo falla
        return {
            "tolerance": 0.6,
            "liveness_activo": 1
        }