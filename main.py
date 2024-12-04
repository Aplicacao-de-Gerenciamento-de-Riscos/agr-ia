from fastapi import FastAPI, HTTPException
import joblib
import numpy as np
import pandas as pd
from crud import load_data
from database import get_db

app = FastAPI()


# Função para carregar o modelo treinado
def load_trained_model():
    print("Carregando modelo treinado...")
    return joblib.load("tuned_random_forest_model.joblib")


# Ajustar colunas do DataFrame para corresponder às colunas usadas no treinamento
def adjust_features_for_model(version_data, model):
    # Obter as colunas esperadas pelo modelo
    expected_features = model.feature_names_in_

    # Adicionar colunas ausentes com valor padrão 0
    for col in expected_features:
        if col not in version_data.columns:
            version_data[col] = 0

    # Remover colunas extras
    version_data = version_data[expected_features]

    return version_data


# Prever o risco de atraso
def predict_delay(version_data):
    model = load_trained_model()

    # Ajustar o DataFrame de entrada
    version_data = adjust_features_for_model(version_data, model)

    # Fazer a predição
    delay_risk_percentage = round(float(model.predict_proba(version_data)[0][1]) * 100, 1)
    print("Probabilidade de Atraso:", delay_risk_percentage)
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

    # Carregar todos os dados das versões
    version_data_all = load_data(db)

    # Garantir que os IDs sejam do mesmo tipo
    if version_data_all['cod_version'].dtype != int:
        version_data_all['cod_version'] = version_data_all['cod_version'].astype(int)

    print("IDs disponíveis em cod_version:", version_data_all['cod_version'].unique())

    # Iterar sobre os IDs fornecidos
    for version_id in version_id_list:
        # Filtrar os dados da versão específica
        version_data = version_data_all[version_data_all['cod_version'] == version_id]

        # Verificar se o DataFrame está vazio
        if version_data.empty:
            print(f"Nenhum dado encontrado para version_id {version_id}.")
            continue

        # Remover colunas desnecessárias
        version_data = version_data.drop(columns=['cod_version', 'cod_project'])

        # Fazer a predição
        try:
            delay_risk_percentage.append({
                "version_id": version_id,
                "delay_risk_percentage": predict_delay(version_data)
            })
        except Exception as e:
            print(f"Erro ao calcular risco de atraso para versão {version_id}: {e}")
            continue

    return delay_risk_percentage


# Exemplo de uso
if __name__ == "__main__":
    db = next(get_db())

    # Carregar todos os dados em formato de DataFrame
    version_data_all = load_data(db)

    # Exemplo de ID de versão
    example_version_id = 16406

    # Filtrar os dados para o ID específico
    version_data = version_data_all[version_data_all['cod_version'] == example_version_id]

    if not version_data.empty:
        version_data = version_data.drop(columns=['cod_version', 'cod_project'])
        delay_risk_percentage = predict_delay(version_data)
        print("Porcentagem de Risco de Atraso:", delay_risk_percentage)
    else:
        print(f"Nenhum dado encontrado para version_id {example_version_id}.")
