import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import to_categorical
import joblib
import os

RUTA = os.path.dirname(os.path.abspath(__file__))

# ==========================
# Cargar datos
# ==========================
datos = pd.read_csv(os.path.join(RUTA, "datos_agua.csv"))

X = datos[['ph', 'temperatura', 'tds', 'conductividad']]
y = datos['clasificacion']

# Convertir a one-hot
y = to_categorical(y, num_classes=3)

# ==========================
# Normalización
# ==========================
scaler = StandardScaler()
X = scaler.fit_transform(X)

# ==========================
# División train/test
# ==========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ==========================
# Modelo red neuronal
# ==========================
modelo = Sequential()
modelo.add(Dense(16, activation='relu', input_dim=4))
modelo.add(Dense(8, activation='relu'))
modelo.add(Dense(3, activation='softmax'))

modelo.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# ==========================
# Entrenar
# ==========================
modelo.fit(X_train, y_train, epochs=100, batch_size=8)

# ==========================
# Evaluar
# ==========================
loss, accuracy = modelo.evaluate(X_test, y_test)
print("Precisión modelo clasificación:", accuracy)

# ==========================
# Guardar modelo y scaler
# ==========================
ruta_guardado = os.path.join(RUTA, "..", "saved")

modelo.save(os.path.join(ruta_guardado, "modelo_clasificacion.h5"))
joblib.dump(scaler, os.path.join(ruta_guardado, "scaler_clasificacion.pkl"))

print("Modelo clasificación guardado en ai_models/saved/")