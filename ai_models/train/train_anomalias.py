import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
import os

RUTA = os.path.dirname(os.path.abspath(__file__))

archivo_csv = os.path.join(RUTA, "datos_agua.csv")
ruta_guardado = os.path.join(RUTA, "..", "saved")
ruta_modelo = os.path.join(ruta_guardado, "modelo_anomalias.pkl")

print("Cargando dataset:", archivo_csv)

datos = pd.read_csv(archivo_csv)

X = datos[['ph', 'temperatura', 'tds', 'conductividad']]

print("Entrenando IsolationForest...")

modelo = IsolationForest(contamination=0.05, random_state=42)
modelo.fit(X)

print("Guardando modelo en:", ruta_modelo)

joblib.dump(modelo, ruta_modelo)

print("Modelo anomalías guardado correctamente.")