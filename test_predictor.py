from ai_models.predictor import PredictorIA

ia = PredictorIA()

resultado = ia.analizar_agua(
    ph=7.2,
    temperatura=26.4,
    tds=200,
    conductividad=600
)

print(resultado)