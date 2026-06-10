def parse_line(linea):
    """
    Formato real Arduino:
    temperatura,ph,conductividad,tds
    Ejemplo: 26.44,7.849,3702,1200
    """

    partes = linea.split(",")

    if len(partes) != 4:
        return None

    try:
        temperatura = float(partes[0])
        ph = float(partes[1])
        conductividad = float(partes[2])
        tds = float(partes[3])

        # Validaciones mínimas (evita basura)
        if ph < 0 or ph > 14:
            return None

        if temperatura < -10 or temperatura > 100:
            return None

        # TDS no debería ser negativo
        if tds < 0:
            tds = 0

        if conductividad < 0:
            conductividad = 0

        return {
            "ph": ph,
            "temperatura": temperatura,
            "tds": tds,
            "conductividad": conductividad
        }

    except:
        return None