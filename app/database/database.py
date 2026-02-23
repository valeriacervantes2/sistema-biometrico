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
    # TIPO_USUARIO
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tipo_usuario (
        id_tipo_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE,
        estado INTEGER DEFAULT 1
    );
    """)

    # =========================
    # ROL
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rol (
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
        id_tipo_usuario INTEGER NOT NULL,
        id_rol INTEGER NOT NULL,
        id_facultad INTEGER,
        id_carrera INTEGER,
        FOREIGN KEY (id_tipo_usuario) REFERENCES tipo_usuario(id_tipo_usuario),
        FOREIGN KEY (id_rol) REFERENCES rol(id_rol),
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
        resultado TEXT NOT NULL,
        confianza REAL,
        FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
    );
    """)

    # =========================
    # HISTORIAL_CAMBIOS
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS historial_cambios (
        id_cambio INTEGER PRIMARY KEY AUTOINCREMENT,
        id_usuario_afectado INTEGER,
        id_usuario_admin INTEGER,
        accion TEXT NOT NULL,
        fecha TEXT NOT NULL,
        FOREIGN KEY (id_usuario_afectado) REFERENCES usuario(id_usuario),
        FOREIGN KEY (id_usuario_admin) REFERENCES usuario(id_usuario)
    );
    """)

    conn.commit()
    conn.close()
    print("Base de datos inicializada correctamente.")