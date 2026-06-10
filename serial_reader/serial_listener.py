import serial
import time
from serial_reader.parser import parse_line

from database.db_manager import (
    insertar_sensor,
    insertar_prediccion,
    insertar_alerta
)

from ai_models.predictor import PredictorIA


PUERTO = "COM3"     # <-- pon tu COM real
BAUDRATE = 9600


def escuchar_serial():
    ser = serial.Serial(PUERTO, BAUDRATE, timeout=2)
    time.sleep(2)

    ia = PredictorIA()

    print("Escuchando Arduino en", PUERTO)

    while True:
        try:
            linea = ser.readline().decode("utf-8").strip()

            if not linea:
                continue

            print("Recibido:", linea)

            datos = parse_line(linea)

            if datos is None:
                print("Formato inválido, ignorado.")
                continue

            # 1) Guardar lectura sensores
            sensor_id = insertar_sensor(
                datos["ph"],
                datos["temperatura"],
                datos["tds"],
                datos["conductividad"]
            )

            print("Guardado en sensores ID:", sensor_id)

            # 2) Ejecutar IA
            resultado = ia.analizar_agua(
                datos["ph"],
                datos["temperatura"],
                datos["tds"],
                datos["conductividad"]
            )

            clasificacion = resultado["clasificacion"]["clasificacion"]
            confianza = resultado["clasificacion"]["confianza"]
            anomalia = resultado["anomalia"]["anomalia"]
            riesgo = resultado["anomalia"]["riesgo"]

            # 3) Guardar predicción en BD
            insertar_prediccion(sensor_id, clasificacion, confianza, anomalia, riesgo)

            print("Predicción guardada.")

            # 4) Generar alerta si hay anomalía
            if anomalia == -1:
                insertar_alerta(
                    sensor_id=sensor_id,
                    tipo="ANOMALIA",
                    descripcion="Valores fuera del patrón normal detectados por IA",
                    nivel="ALTO"
                )
                print("⚠ ALERTA generada (anomalia detectada).")

        except Exception as e:
            print("Error:", e)
            time.sleep(2)


if __name__ == "__main__":
    escuchar_serial()