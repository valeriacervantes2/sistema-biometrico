from app.database.database import get_connection
from datetime import datetime


# ─────────────────────────────────────────────
#  CONSULTAS DE LECTURA
# ─────────────────────────────────────────────

def obtener_todos_usuarios():
    """
    Consulta todos los usuarios con info de rol, facultad y carrera (via JOINs).
    Retorna: lista de diccionarios con los datos de usuarios.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT u.id_usuario, u.nombre, u.a_paterno, u.a_materno, u.estado,
                   u.fecha_registro, u.fecha_actualizacion,
                   r.nombre  AS rol_nombre,
                   f.nombre  AS facultad_nombre,
                   c.nombre  AS carrera_nombre
            FROM usuario u
            LEFT JOIN usuario_rol r ON u.id_rol      = r.id_rol
            LEFT JOIN facultad    f ON u.id_facultad = f.id_facultad
            LEFT JOIN carrera     c ON u.id_carrera  = c.id_carrera
        """)
        filas = cursor.fetchall()

        usuarios = []
        for fila in filas:
            usuarios.append({
                "id":                 fila[0],
                "nombre":             fila[1],
                "a_paterno":          fila[2],
                "a_materno":          fila[3],
                "estado":             fila[4],
                "fecha_registro":     fila[5],
                "fecha_actualizacion": fila[6],
                "rol_nombre":         fila[7],
                "facultad_nombre":    fila[8],
                "carrera_nombre":     fila[9],
            })

        return usuarios

    except Exception as e:
        print(f"❌ Error al obtener usuarios: {e}")
        return []
    finally:
        conn.close()


def obtener_usuario_por_id(id_usuario):
    """
    Obtiene los datos crudos (con IDs foráneos) de un usuario específico.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id_usuario, nombre, a_paterno, a_materno, estado,
                   fecha_registro, fecha_actualizacion,
                   id_rol, id_facultad, id_carrera
            FROM usuario
            WHERE id_usuario = ?
        """, (id_usuario,))

        fila = cursor.fetchone()
        if fila is None:
            return None

        return {
            "id":                  fila[0],
            "nombre":              fila[1],
            "a_paterno":           fila[2],
            "a_materno":           fila[3],
            "estado":              fila[4],
            "fecha_registro":      fila[5],
            "fecha_actualizacion": fila[6],
            "id_rol":              fila[7],
            "id_facultad":         fila[8],
            "id_carrera":          fila[9],
        }

    except Exception as e:
        print(f"❌ Error al obtener usuario por id: {e}")
        return None
    finally:
        conn.close()


# ─────────────────────────────────────────────
#  CRUD PRINCIPAL
# ─────────────────────────────────────────────

def crear_usuario(nombre, a_paterno, a_materno, id_rol, id_facultad=None, id_carrera=None, estado=1):
    """
    Inserta un nuevo usuario en la base de datos.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
            INSERT INTO usuario (nombre, a_paterno, a_materno, estado, fecha_registro, id_rol, id_facultad, id_carrera)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (nombre, a_paterno, a_materno, estado, fecha, id_rol, id_facultad, id_carrera))

        conn.commit()
        print(f"✅ Usuario '{nombre}' creado exitosamente.")
        return True

    except Exception as e:
        print(f"❌ Error al crear usuario: {e}")
        return False
    finally:
        conn.close()


def actualizar_usuario(id_usuario, nombre, a_paterno, a_materno, id_rol,
                       id_facultad=None, id_carrera=None, estado=1):
    """
    Actualiza un usuario existente buscándolo por id_usuario.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
            UPDATE usuario
            SET nombre = ?, a_paterno = ?, a_materno = ?, estado = ?,
                fecha_actualizacion = ?, id_rol = ?, id_facultad = ?, id_carrera = ?
            WHERE id_usuario = ?
        """, (nombre, a_paterno, a_materno, estado, fecha, id_rol, id_facultad, id_carrera, id_usuario))

        conn.commit()
        return cursor.rowcount > 0

    except Exception as e:
        print(f"❌ Error al actualizar usuario: {e}")
        return False
    finally:
        conn.close()


def eliminar_usuario(id_usuario):
    """
    Elimina un usuario de la base de datos.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuario WHERE id_usuario = ?", (id_usuario,))
        conn.commit()
        return cursor.rowcount > 0

    except Exception as e:
        print(f"❌ Error al eliminar usuario: {e}")
        return False
    finally:
        conn.close()


# ─────────────────────────────────────────────
#  HELPERS PARA DROPDOWNS
# ─────────────────────────────────────────────

def obtener_id_rol_por_nombre(nombre_rol):
    """
    Busca el ID numérico de un rol a partir de su nombre (case-insensitive).
    Útil para mapear texto del dropdown → FK antes de insertar.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id_rol FROM usuario_rol WHERE UPPER(nombre) = UPPER(?)",
            (nombre_rol.strip(),)
        )
        res = cursor.fetchone()
        return res[0] if res else None

    except Exception as e:
        print(f"❌ Error al obtener id de rol: {e}")
        return None
    finally:
        conn.close()


def obtener_roles_para_dropdown():
    """
    Retorna diccionario {id_rol: nombre_rol} para poblar un ComboBox.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id_rol, nombre FROM usuario_rol")
        filas = cursor.fetchall()
        return {fila[0]: fila[1] for fila in filas}

    except Exception as e:
        print(f"❌ Error al obtener roles: {e}")
        return {}
    finally:
        conn.close()


def obtener_facultades_para_dropdown():
    """
    Retorna diccionario {id_facultad: nombre} de facultades activas.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id_facultad, nombre FROM facultad WHERE estado = 1")
        filas = cursor.fetchall()
        return {fila[0]: fila[1] for fila in filas}

    except Exception as e:
        print(f"❌ Error al obtener facultades: {e}")
        return {}
    finally:
        conn.close()


def obtener_carreras_para_dropdown():
    """
    Retorna diccionario {id_carrera: nombre} de todas las carreras activas.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id_carrera, nombre FROM carrera WHERE estado = 1")
        filas = cursor.fetchall()
        return {fila[0]: fila[1] for fila in filas}

    except Exception as e:
        print(f"❌ Error al obtener carreras: {e}")
        return {}
    finally:
        conn.close()


def obtener_carreras_por_facultad(id_facultad):
    """
    Retorna diccionario {id_carrera: nombre} de carreras activas de una facultad específica.
    Ideal para filtrar el ComboBox de carrera al cambiar la facultad.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id_carrera, nombre FROM carrera WHERE estado = 1 AND id_facultad = ?",
            (id_facultad,)
        )
        filas = cursor.fetchall()
        return {fila[0]: fila[1] for fila in filas}

    except Exception as e:
        print(f"❌ Error al obtener carreras por facultad: {e}")
        return {}
    finally:
        conn.close()