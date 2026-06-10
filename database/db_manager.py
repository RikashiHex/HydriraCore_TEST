import sqlite3

DB_PATH = "database/agua.db"


# ==========================
# CONEXIÓN
# ==========================
def conectar():
    return sqlite3.connect(DB_PATH)


# ==========================
# INSERTAR LECTURA DE SENSORES
# ==========================
def insertar_sensor(ph, temperatura, tds, conductividad):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO sensores (ph, temperatura, tds, conductividad)
        VALUES (?, ?, ?, ?)
    """, (ph, temperatura, tds, conductividad))

    conn.commit()

    sensor_id = cursor.lastrowid

    conn.close()
    return sensor_id


# ==========================
# INSERTAR PREDICCIÓN IA (agua)
# ==========================
def insertar_prediccion(sensor_id, clasificacion, confianza, anomalia, riesgo):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO predicciones (sensor_id, clasificacion, confianza, anomalia, riesgo)
        VALUES (?, ?, ?, ?, ?)
    """, (sensor_id, clasificacion, confianza, anomalia, riesgo))

    conn.commit()
    conn.close()


# ==========================
# INSERTAR ALERTA
# ==========================
def insertar_alerta(sensor_id, tipo, descripcion, nivel):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO alertas (sensor_id, tipo, descripcion, nivel)
        VALUES (?, ?, ?, ?)
    """, (sensor_id, tipo, descripcion, nivel))

    conn.commit()
    conn.close()


# ==========================
# INSERTAR DATOS FILTRO (antes/después)
# ==========================
def insertar_filtro(ph_in, ph_out, tds_in, tds_out, conduct_in, conduct_out, litros):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO filtros (ph_in, ph_out, tds_in, tds_out, conduct_in, conduct_out, litros)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (ph_in, ph_out, tds_in, tds_out, conduct_in, conduct_out, litros))

    conn.commit()

    filtro_id = cursor.lastrowid

    conn.close()
    return filtro_id


# ==========================
# INSERTAR PREDICCIÓN FILTRO
# ==========================
def insertar_prediccion_filtro(filtro_id, vida_filtro, estado):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO predicciones_filtros (filtro_id, vida_filtro, estado)
        VALUES (?, ?, ?)
    """, (filtro_id, vida_filtro, estado))

    conn.commit()
    conn.close()


# ==========================
# OBTENER ÚLTIMA LECTURA
# ==========================
def obtener_ultima_lectura():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, ph, temperatura, tds, conductividad, fecha
        FROM sensores
        ORDER BY id DESC
        LIMIT 1
    """)

    fila = cursor.fetchone()
    conn.close()

    return fila


# ==========================
# OBTENER ÚLTIMA PREDICCIÓN
# ==========================
def obtener_ultima_prediccion():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, sensor_id, clasificacion, confianza, anomalia, riesgo, fecha
        FROM predicciones
        ORDER BY id DESC
        LIMIT 1
    """)

    fila = cursor.fetchone()
    conn.close()

    return fila