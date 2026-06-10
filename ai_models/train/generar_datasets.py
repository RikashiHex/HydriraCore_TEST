import random
import pandas as pd
import os

RUTA = os.path.dirname(os.path.abspath(__file__))


def generar_datos_agua(n=200):
    filas = []

    for _ in range(n):
        ph = round(random.uniform(4.5, 9.5), 2)
        temperatura = round(random.uniform(15, 40), 2)
        tds = round(random.uniform(50, 2500), 2)
        conductividad = round(random.uniform(100, 5000), 2)

        if ph < 5.5 or ph > 9.0 or tds > 1500 or conductividad > 3500:
            clasificacion = 0
        elif tds < 400 and conductividad < 1000:
            clasificacion = 2
        else:
            clasificacion = 1

        filas.append([ph, temperatura, tds, conductividad, clasificacion])

    df = pd.DataFrame(filas, columns=["ph", "temperatura", "tds", "conductividad", "clasificacion"])
    df.to_csv(os.path.join(RUTA, "datos_agua.csv"), index=False)

    print("datos_agua.csv generado con", n, "filas")


def generar_datos_filtros(n=200):
    filas = []

    for _ in range(n):
        ph_in = round(random.uniform(5.0, 9.0), 2)
        tds_in = round(random.uniform(200, 2500), 2)
        conduct_in = round(random.uniform(300, 5000), 2)

        litros = round(random.uniform(5, 300), 2)

        desgaste = litros / 300

        ph_out = round(ph_in - random.uniform(0.0, 0.3) * desgaste, 2)
        tds_out = round(tds_in - random.uniform(50, 600) * (1 - desgaste), 2)
        conduct_out = round(conduct_in - random.uniform(100, 1500) * (1 - desgaste), 2)

        vida_filtro = round(100 - (litros / 3), 2)

        if vida_filtro < 0:
            vida_filtro = 0

        filas.append([
            ph_in, ph_out,
            tds_in, tds_out,
            conduct_in, conduct_out,
            litros,
            vida_filtro
        ])

    df = pd.DataFrame(filas, columns=[
        "ph_in", "ph_out",
        "tds_in", "tds_out",
        "conduct_in", "conduct_out",
        "litros",
        "vida_filtro"
    ])

    df.to_csv(os.path.join(RUTA, "datos_filtros.csv"), index=False)

    print("datos_filtros.csv generado con", n, "filas")


if __name__ == "__main__":
    generar_datos_agua(200)
    generar_datos_filtros(200)