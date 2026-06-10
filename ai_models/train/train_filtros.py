import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential
from keras.layers import Dense
import joblib
import os

RUTA = os.path.dirname(os.path.abspath(__file__))

datos = pd.read_csv(os.path.join(RUTA, "datos_filtros.csv"))

X = datos[
[
    'ph_in','ph_out',
    'tds_in','tds_out',
    'conduct_in','conduct_out',
    'litros'
]]

y = datos['vida_filtro']

scaler = StandardScaler()
X = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

modelo = Sequential()
modelo.add(Dense(32, activation='relu', input_dim=7))
modelo.add(Dense(16, activation='relu'))
modelo.add(Dense(1))

modelo.compile(optimizer='adam', loss='mean_squared_error')

modelo.fit(X_train, y_train, epochs=150, batch_size=8)

loss = modelo.evaluate(X_test, y_test)
print("Error modelo filtros:", loss)

ruta_guardado = os.path.join(RUTA, "..", "saved")

modelo.save(os.path.join(ruta_guardado, "modelo_filtros.h5"))
joblib.dump(scaler, os.path.join(ruta_guardado, "scaler_filtros.pkl"))

print("Modelo filtros guardado en ai_models/saved/")