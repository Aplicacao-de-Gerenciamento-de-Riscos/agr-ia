from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
from crud import load_data
from database import get_db
import joblib

app = FastAPI()


# Função para carregar o modelo treinado
def load_trained_model():
    return joblib.load("tuned_xgboost_model.joblib")


# Função para prever o risco de atraso de uma versão específica
def predict_delay(version_data):
    model = load_trained_model()

    # Obtenha a probabilidade de atraso
    delay_risk_percentage = float(model.predict_proba(version_data)[0][1]) * 100  # Converte para float

    return delay_risk_percentage


@app.get("/predict-delay")
def get_predict_delay(version_ids: str):
    # Converter a string 'id1,id2,id3' em uma lista de inteiros
    try:
        version_id_list = [int(id) for id in version_ids.split(',')]
    except ValueError:
        raise HTTPException(status_code=400, detail="IDs devem ser números inteiros separados por vírgulas")

    db = next(get_db())

    delay_risk_percentage = []

    for version_id in version_id_list:
        # Carregar os dados da versão específica em formato de DataFrame
        version_data = load_data(db)
        version_data = version_data[version_data['cod_version'] == version_id].drop(columns=['cod_version', 'cod_project'])

        # Fazer a predição e obter o risco e épicos que mais impactam
        delay_risk_percentage.append({
            "version_id": version_id,
            "delay_risk_percentage": predict_delay(version_data)
        })

    return delay_risk_percentage


# Exemplo de uso
if __name__ == "__main__":
    db = next(get_db())
    # Carregar os dados da versão específica em formato de DataFrame
    version_data = load_data(db)
    version_data = version_data[version_data['cod_version'] == 16406].drop(columns=['cod_version', 'cod_project'])

    # Fazer a predição e obter o risco e épicos que mais impactam
    delay_risk_percentage = predict_delay(version_data)

    print("Porcentagem de Risco de Atraso:", delay_risk_percentage)