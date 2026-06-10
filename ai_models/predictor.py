import numpy as np
import joblib
from keras.models import load_model


class PredictorIA:
    def __init__(self):
        # Cargar modelos y scalers
        self.modelo_clasificacion = load_model("ai_models/saved/modelo_clasificacion.h5")
        self.scaler_clasificacion = joblib.load("ai_models/saved/scaler_clasificacion.pkl")

        self.modelo_filtros = load_model("ai_models/saved/modelo_filtros.h5")
        self.scaler_filtros = joblib.load("ai_models/saved/scaler_filtros.pkl")

        self.modelo_anomalias = joblib.load("ai_models/saved/modelo_anomalias.pkl")

        self.etiquetas = {
            0: "No reutilizable",
            1: "Reutilizable para limpieza",
            2: "Reutilizable para riego"
        }

    def clasificar_agua(self, ph, temperatura, tds, conductividad):
        X = np.array([[ph, temperatura, tds, conductividad]])
        X_scaled = self.scaler_clasificacion.transform(X)

        pred = self.modelo_clasificacion.predict(X_scaled, verbose=0)[0]

        clasificacion = int(np.argmax(pred))
        confianza = float(np.max(pred))

        return {
            "clasificacion": clasificacion,
            "descripcion": self.etiquetas[clasificacion],
            "confianza": confianza,
            "probabilidades": {
                "no_reutilizable": float(pred[0]),
                "limpieza": float(pred[1]),
                "riego": float(pred[2])
            }
        }

    def detectar_anomalia(self, ph, temperatura, tds, conductividad):
        resultado = self.modelo_anomalias.predict([[ph, temperatura, tds, conductividad]])

        if resultado[0] == 1:
            return {"anomalia": 1, "riesgo": "normal"}
        else:
            return {"anomalia": -1, "riesgo": "anomalia_detectada"}

    def predecir_filtro(self, ph_in, ph_out, tds_in, tds_out, conduct_in, conduct_out, litros):
        X = np.array([[ph_in, ph_out, tds_in, tds_out, conduct_in, conduct_out, litros]])
        X_scaled = self.scaler_filtros.transform(X)

        vida = self.modelo_filtros.predict(X_scaled, verbose=0)[0][0]
        vida = float(max(0, min(100, vida)))

        if vida > 70:
            estado = "filtro en buen estado"
        elif vida > 30:
            estado = "filtro desgastado"
        else:
            estado = "filtro casi saturado"

        return {"vida_filtro": vida, "estado": estado}

    def analizar_agua(self, ph, temperatura, tds, conductividad):
        clasif = self.clasificar_agua(ph, temperatura, tds, conductividad)
        anom = self.detectar_anomalia(ph, temperatura, tds, conductividad)

        return {
            "clasificacion": clasif,
            "anomalia": anom
        }