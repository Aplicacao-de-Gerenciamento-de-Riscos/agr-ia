from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_db  # Importar função para obter sessão do banco de dados
from crud import load_data  # Sua função de carregamento de dados
from predict_model import predict_delay  # Função de previsão do modelo treinado

app = FastAPI()

@app.get("/predict_delay/{cod_version}")
def predict(cod_version: int, db: Session = Depends(get_db)):
    # Passo 1: Carregar dados
    version_data = load_data(db)

    # Passo 2: Filtrar dados para a versão especificada
    version_info = version_data[version_data['cod_version'] == cod_version]

    # Passo 3: Executar previsão do modelo
    delay_risk = predict_delay(version_info)

    # Passo 4: Retornar resposta
    return {
        "version_id": cod_version,
        "delay_risk_percentage": delay_risk
    }
