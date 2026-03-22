from fastapi import FastAPI
from pydantic import BaseModel
import mlflow.pyfunc
import os

app = FastAPI(title="Penguins Inference API")

MODEL_NAME = "penguins-best-model"
MODEL_STAGE_OR_ALIAS = "latest"

SPECIES_MAP = {
    0: "Adelie",
    1: "Chinstrap",
    2: "Gentoo"
}


class PenguinFeatures(BaseModel):
    island: int
    bill_length_mm: float
    bill_depth_mm: float
    flipper_length_mm: int
    body_mass_g: int
    sex: int
    year: int


def load_model():
    model_uri = f"models:/{MODEL_NAME}/{MODEL_STAGE_OR_ALIAS}"
    return mlflow.pyfunc.load_model(model_uri)


@app.on_event("startup")
def startup_event():
    global model
    tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")
    mlflow.set_tracking_uri(tracking_uri)
    model = load_model()


@app.get("/")
def root():
    return {"message": "Penguins API running"}


@app.get("/health")
def health():
    return {"status": "ok", "model_name": MODEL_NAME}


@app.post("/predict")
def predict(features: PenguinFeatures):
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