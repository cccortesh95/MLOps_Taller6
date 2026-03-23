"""
API de inferencia para clasificación de especies de pingüinos.

Consume un modelo registrado en MLflow para predecir la especie
(Adelie, Chinstrap o Gentoo) a partir de medidas morfológicas.
La carga del modelo es lazy: si el modelo no está disponible,
la API inicia igual y responde HTTP 503 en /predict.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import mlflow.pyfunc
import os

app = FastAPI(
    title="Penguins Inference API",
    description="Clasificación de especies de pingüinos usando un modelo de MLflow",
    version="1.0.0",
)

MODEL_NAME = "penguins-best-model"
MODEL_STAGE_OR_ALIAS = "latest"

SPECIES_MAP = {
    0: "Adelie",
    1: "Chinstrap",
    2: "Gentoo"
}


class PenguinFeatures(BaseModel):

    island: int = Field(default=0, ge=0, le=2, description="Isla (0=Biscoe, 1=Dream, 2=Torgersen)")
    bill_length_mm: float = Field(default=43.9, ge=30.0, le=60.0, description="Largo del pico en mm")
    bill_depth_mm: float = Field(default=17.2, ge=13.0, le=22.0, description="Profundidad del pico en mm")
    flipper_length_mm: int = Field(default=200, ge=170, le=230, description="Largo de aleta en mm")
    body_mass_g: int = Field(default=4200, ge=2700, le=6300, description="Masa corporal en g")
    sex: int = Field(default=0, ge=0, le=1, description="Sexo (0=hembra, 1=macho)")
    year: int = Field(default=2008, ge=2007, le=2009, description="Año de observación")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "island": 0,
                    "bill_length_mm": 39.1,
                    "bill_depth_mm": 18.7,
                    "flipper_length_mm": 181,
                    "body_mass_g": 3750,
                    "sex": 1,
                    "year": 2007,
                }
            ]
        }
    }


def load_model():
    model_uri = f"models:/{MODEL_NAME}/{MODEL_STAGE_OR_ALIAS}"
    return mlflow.pyfunc.load_model(model_uri)


def try_load_model():
    try:
        return load_model()
    except Exception:
        return None


@app.on_event("startup")
def startup_event():
    tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")
    mlflow.set_tracking_uri(tracking_uri)


@app.get("/")
def root():
    return {"message": "Penguins API running"}


@app.get("/health")
def health():
    model = try_load_model()
    if model is not None:
        return {"status": "ok", "model_name": MODEL_NAME, "model_status": "loaded"}
    return {"status": "ok", "model_name": MODEL_NAME, "model_status": "unavailable"}


@app.post("/predict")
def predict(features: PenguinFeatures):
    model = try_load_model()
    if model is None:
        raise HTTPException(status_code=503, detail="Model not available")

    data = [[
        features.island,
        features.bill_length_mm,
        features.bill_depth_mm,
        features.flipper_length_mm,
        features.body_mass_g,
        features.sex,
        features.year
    ]]

    prediction = model.predict(data)
    pred_class = int(prediction[0])

    return {
        "prediction": pred_class,
        "species_name": SPECIES_MAP.get(pred_class, "Unknown")
    }
