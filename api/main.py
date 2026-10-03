import joblib
import pandas as pd
from fastapi import FastAPI


MODEL_PATH = "model/rain_model.pkl"

app = FastAPI(
    title="Projet Goutte d'Eau - API",
    description="API MVP pour estimer le risque de pluie",
    version="1.0.0"
)

model = joblib.load(MODEL_PATH)


@app.get("/")
def home():
    return {
        "message": "API Projet Goutte d'Eau opérationnelle"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.get("/predict")
def predict(
    heure: int,
    temperature: float,
    humidite: float,
    precipitation: float,
    vent: float
):
    input_data = pd.DataFrame([
        {
            "heure_observation": heure,
            "temperature": temperature,
            "humidite": humidite,
            "precipitation": precipitation,
            "vent": vent
        }
    ])

    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]

    if probability >= 0.7:
        level = "élevé"
    elif probability >= 0.4:
        level = "moyen"
    else:
        level = "faible"

    return {
        "risk": round(float(probability), 2),
        "level": level,
        "prediction": int(prediction),
        "message": f"Risque de pluie {level}"
    }