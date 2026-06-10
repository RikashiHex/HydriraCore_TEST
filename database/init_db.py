import sqlite3

DB_PATH = "database/agua.db"

def crear_bd():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # ==========================
    # TABLA 1: sensores
    # ==========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sensores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ph REAL NOT NULL,
        temperatura REAL NOT NULL,
        tds REAL NOT NULL,
        conductividad REAL NOT NULL,
        fecha DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ==========================
    # TABLA 2: predicciones (IA #1 y IA #3)
    # ==========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predicciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sensor_id INTEGER NOT NULL,
        clasificacion INTEGER NOT NULL,
        confianza REAL NOT NULL,
        anomalia INTEGER NOT NULL,
        riesgo TEXT NOT NULL,
        fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(sensor_id) REFERENCES sensores(id)
    )
    """)

    # ==========================
    # TABLA 3: alertas
    # ==========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alertas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sensor_id INTEGER,
        tipo TEXT NOT NULL,
        descripcion TEXT NOT NULL,
        nivel TEXT NOT NULL,
        fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(sensor_id) REFERENCES sensores(id)
    )
    """)

    # ==========================
    # TABLA 4: filtros (datos crudos antes/después)
    # ==========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS filtros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ph_in REAL NOT NULL,
        ph_out REAL NOT NULL,
        tds_in REAL NOT NULL,
        tds_out REAL NOT NULL,
        conduct_in REAL NOT NULL,
        conduct_out REAL NOT NULL,
        litros REAL NOT NULL,
        fecha DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ==========================
    # TABLA 5: predicciones_filtros (IA #2)
    # ==========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predicciones_filtros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filtro_id INTEGER NOT NULL,
        vida_filtro REAL NOT NULL,
        estado TEXT NOT NULL,
        fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(filtro_id) REFERENCES filtros(id)
    )
    """)

    # ==========================
    # TABLA 6: sistema_estado (opcional recomendado)
    # ==========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sistema_estado (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bomba_1 INTEGER DEFAULT 0,
        bomba_2 INTEGER DEFAULT 0,
        modo TEXT DEFAULT 'AUTO',
        descripcion TEXT,
        fecha DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()
    print("Base de datos creada correctamente.")

if __name__ == "__main__":
    crear_bd()