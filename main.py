# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, models, ai_model
from database import get_db

app = FastAPI()


# Endpoint para fazer previsões de atraso por projeto
@app.get("/projects/{cod_project}/predict")
def predict_project_delay(cod_project: int, db: Session = Depends(get_db)):
    # Obter as issues do projeto
    issues = crud.get_issues_by_project(db, cod_project)

    if not issues:
        raise HTTPException(status_code=404, detail="No issues found for this project")

    # Fazer a previsão com o modelo de IA
    # predictions = ai_model.predict_delay(issues)

    # return {"project": cod_project, "predictions": predictions.tolist()}
    return {"project": cod_project, "predictions": [1, 2, 3]}

# Endpoint básico para buscar todas as issues de um projeto específico
@app.get("/projects/{cod_project}/issues")
def get_issues_by_project(cod_project: int, db: Session = Depends(get_db)):
    # Buscar todas as issues associadas ao cod_project
    issues = crud.get_issues_by_project(db, cod_project)

    if not issues:
        raise HTTPException(status_code=404, detail="No issues found for this project")

    return issues
