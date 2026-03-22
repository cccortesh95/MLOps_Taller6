# 🐧 MLOps Penguins Classification


## Arquitectura de la solución

La solución está compuesta por los siguientes servicios:

- **PostgreSQL MLflow DB**: almacena la metadata de MLflow
- **PostgreSQL Penguins DB**: almacena los datos `raw` y `processed`
- **MLflow Tracking Server**: registra experimentos, métricas, parámetros y modelos
- **MinIO**: almacena artifacts y modelos generados por MLflow
- **JupyterLab**: ambiente de experimentación y entrenamiento
- **FastAPI**: API de inferencia que carga el mejor modelo desde MLflow Registry

---

## Servicios desplegados

| Servicio | Propósito | Puerto |
|----------|-----------|--------|
| `mlflow_db` | Base de datos de metadata de MLflow | `5433` |
| `penguins_db` | Base de datos de datos raw y processed | `5434` |
| `minio` | Artifact store para MLflow | `9000` |
| `minio console` | Consola web de MinIO | `9001` |
| `mlflow` | Tracking server y model registry | `5000` |
| `jupyter` | Notebook de experimentación | `8888` |
| `api` | API de inferencia | `8000` |

---

## Estructura del proyecto

```bash
mlops_penguins/
├── .env
├── docker-compose.yml
├── init_sql/
│   └── penguins_init.sql
├── jupyter/
│   ├── Dockerfile
│   └── requirements.txt
├── mlflow/
│   ├── Dockerfile
│   └── requirements.txt
├── api/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app.py
└── notebooks/
    ├── penguins_v1.csv
    ├── penguins_training_mlflow.ipynb
    └── penguins_experiment_results.csv
```
## Variables de entorno

```bash
MLFLOW_DB_USER=mlflow
MLFLOW_DB_PASSWORD=mlflow123
MLFLOW_DB_NAME=mlflow_db
MLFLOW_DB_PORT=5433

DATA_DB_USER=penguins
DATA_DB_PASSWORD=penguins123
DATA_DB_NAME=penguins_db
DATA_DB_PORT=5434

MINIO_ROOT_USER=minio
MINIO_ROOT_PASSWORD=minio123
MINIO_PORT=9000
MINIO_CONSOLE_PORT=9001
MLFLOW_BUCKET=mlflow

MLFLOW_PORT=5000
JUPYTER_PORT=8888
API_PORT=8000

```
## Levantamiento de la solución

```bash
docker compose up -d --build
```

## Accesos a la solución
MLflow UI:
```bash
http://localhost:5000
```
MinIO Console:
```bash
http://localhost:9001
```
JupyterLab:
```bash
http://localhost:8888
```
FastAPI Docs:
```bash
http://localhost:8000/docs
```

# Bases de datos utilizadas
1. Base de datos para metadata de MLflow
    Se usa una instancia dedicada de PostgreSQL para almacenar:
   
        -experimentos
        -runs
        -parámetros
        -métricas
        -registro de modelos
3. Base de datos para datos del proyecto

    Se usa otra instancia de PostgreSQL para almacenar:
   
        -penguins_raw
        -penguins_processed

# Carga y procesamiento de datos

Tabla penguins_raw

- Contiene el dataset original cargado desde CSV.

Tabla penguins_processed

- Contiene el dataset listo para modelado:

    - sin columna id
    - sin nulos
    - con variables numéricas listas para entrenamiento

# Modelos entrenados
Se entrenaron mínimo tres modelos de clasificación:

- SVM
- RandomForestClassifier
- LogisticRegression
