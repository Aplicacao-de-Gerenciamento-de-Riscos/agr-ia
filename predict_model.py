import joblib
from crud import load_data
from database import get_db

# Função para carregar o modelo treinado
def load_trained_model():
    return joblib.load("tuned_xgboost_model.joblib")

# Função para prever o risco de atraso de uma versão específica
def predict_delay(version_data):
    model = load_trained_model()

    # Obtenha a probabilidade de atraso
    delay_risk_percentage = model.predict_proba(version_data)[0][1] * 100  # Pega a probabilidade de atraso (classe 1)

    return delay_risk_percentage

# Exemplo de uso
if __name__ == "__main__":
    db = next(get_db())
    # Carregar os dados da versão específica em formato de DataFrame
    version_data = load_data(db)
    version_data = version_data[version_data['cod_version'] == 16406].drop(columns=['cod_version', 'cod_project'])

    # Fazer a predição e obter o risco e épicos que mais impactam
    delay_risk_percentage, impacting_epics = predict_delay(version_data)

    print("Porcentagem de Risco de Atraso:", delay_risk_percentage)
