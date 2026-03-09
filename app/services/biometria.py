from app.database.database import get_connection
from datetime import datetime

def guardar_embedding(id_usuario, embedding):
    conn = get_connection()
    cursor = conn.cursor()
    fecha = datetime.now().isoformat()
    cursor.execute("""
        INSERT INTO biometria (id_usuario, embedding, fecha_registro)
        VALUES (?, ?, ?)
    """, (id_usuario, embedding, fecha))
    conn.commit()
    conn.close()

def obtener_embeddings_activos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_usuario, embedding FROM biometria WHERE estado = 1")
    datos = cursor.fetchall()
    conn.close()
    return datos

def desactivar_embedding(id_biometria):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE biometria SET estado = 0, fecha_registro = ? WHERE id_biometria = ?",
                    (datetime.now().isoformat(), id_biometria))
    conn.commit()
    conn.close()