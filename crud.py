# crud.py
from sqlalchemy.orm import Session
import models

# Obter issues por projeto
def get_issues_by_project(db: Session, cod_project: int):
    return (db.query(models.Issue)
              .join(models.VersionIssue, models.Issue.cod_issue == models.VersionIssue.cod_issue)
              .join(models.Version, models.VersionIssue.cod_version == models.Version.cod_version)
              .filter(models.Version.cod_project == cod_project)
              .all())