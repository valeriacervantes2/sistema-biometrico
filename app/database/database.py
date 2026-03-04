import sqlite3
from datetime import datetime
import os

# Ruta absoluta segura
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "sistema_biometrico.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def inicializar_bd():
    conn = get_connection()
    cursor = conn.cursor()

    # =========================
    # USUARIO_ROL
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuario_rol (
        id_rol INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE,
        descripcion TEXT
    );
    """)

    # =========================
    # FACULTAD
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS facultad (
        id_facultad INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE,
        estado INTEGER DEFAULT 1
    );
    """)

    # =========================
    # CARRERA
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS carrera (
        id_carrera INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        id_facultad INTEGER NOT NULL,
        estado INTEGER DEFAULT 1,
        FOREIGN KEY (id_facultad) REFERENCES facultad(id_facultad)
            ON DELETE CASCADE
    );
    """)

    # =========================
    # USUARIO
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuario (
        id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        a_paterno TEXT NOT NULL,
        a_materno TEXT,
        estado INTEGER DEFAULT 1,
        fecha_registro TEXT NOT NULL,
        fecha_actualizacion TEXT,
        id_rol INTEGER NOT NULL,
        id_facultad INTEGER,
        id_carrera INTEGER,
        FOREIGN KEY (id_rol) REFERENCES usuario_rol(id_rol),
        FOREIGN KEY (id_facultad) REFERENCES facultad(id_facultad),
        FOREIGN KEY (id_carrera) REFERENCES carrera(id_carrera)
    );
    """)

    # =========================
    # BIOMETRIA
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS biometria (
        id_biometria INTEGER PRIMARY KEY AUTOINCREMENT,
        id_usuario INTEGER NOT NULL,
        embedding BLOB NOT NULL,
        fecha_registro TEXT NOT NULL,
        estado INTEGER DEFAULT 1,
        FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
            ON DELETE CASCADE
    );
    """)

    # =========================
    # REGISTRO_ACCESO
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS registro_acceso (
        id_registro INTEGER PRIMARY KEY AUTOINCREMENT,
        id_usuario INTEGER,
        fecha_hora TEXT NOT NULL,
        resultado INTEGER NOT NULL, -- 1 acceso permitido, 0 denegado
        confianza REAL,
        motivo TEXT, -- baja confianza, no reconocido, liveness fallido
        FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);
""")

    conn.commit()
    conn.close()
    print("Base de datos creada correctamente.")







    if __name__ == "__main__":
        print("Estoy ejecutando database.py")
        inicializar_bd()

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        print("Tablas creadas:")
        print(cursor.fetchall())
        conn.close()