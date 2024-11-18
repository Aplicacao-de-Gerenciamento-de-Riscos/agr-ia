from sqlalchemy.orm import Session
from models import Issue, Sprint, VersionIssue, Version, Project
import pandas as pd

# Função para carregar os dados do banco de dados
def load_data(db: Session):
    # Carregar sprints e projetos com uma única consulta
    projects_with_sprints = (db.query(Project.cod_project, Project.key, Sprint.cod_sprint, Sprint.name)
                                .join(Sprint, Sprint.name.contains(Project.key))
                                .all())

    # Criar o mapeamento de projetos para sprints
    project_sprint_map = {}
    for project_cod, project_key, sprint_cod, sprint_name in projects_with_sprints:
        if project_cod not in project_sprint_map:
            project_sprint_map[project_cod] = []
        project_sprint_map[project_cod].append(sprint_cod)

    # Carregar todas as issues e relações em uma única consulta
    issues = (db.query(Issue.cod_issue, Issue.time_original_estimate, Issue.timespent, Issue.priority, Issue.cod_sprint,
                       Issue.cod_epic, Issue.issuetype, VersionIssue.cod_version, Project.cod_project)
                .join(Sprint, Issue.cod_sprint == Sprint.cod_sprint)
                .join(VersionIssue, Issue.cod_issue == VersionIssue.cod_issue)
                .join(Version, VersionIssue.cod_version == Version.cod_version)
                .join(Project, Version.cod_project == Project.cod_project)
                .all())

    # Converter as issues para um DataFrame
    issue_data = pd.DataFrame([{
        'cod_issue': issue.cod_issue,
        'time_original_estimate': issue.time_original_estimate,
        'timespent': issue.timespent,
        'priority': issue.priority,
        'cod_sprint': issue.cod_sprint,
        'cod_epic': issue.cod_epic,
        'issuetype': issue.issuetype,
        'cod_project': issue.cod_project,
        'cod_version': issue.cod_version
    } for issue in issues])

    # Verifique a existência do mapeamento de projeto para sprint antes de atribuir
    issue_data['cod_project'] = issue_data['cod_sprint'].map(
        lambda sprint: next((project for project, sprints in project_sprint_map.items() if sprint in sprints), None)
    )

    # Aplicar one-hot encoding para colunas categóricas
    issue_data = pd.get_dummies(issue_data, columns=['priority', 'issuetype', 'cod_epic'])

    # Agrupar por versão e projeto
    aggregation_functions = {
        'time_original_estimate': 'sum',
        'timespent': 'sum',
        **{col: 'mean' for col in issue_data.columns if col.startswith('priority_')},
        **{col: 'mean' for col in issue_data.columns if col.startswith('issuetype_')},
        **{col: 'sum' for col in issue_data.columns if col.startswith('cod_epic_')}
    }
    version_data = issue_data.groupby(['cod_version', 'cod_project']).agg(aggregation_functions).reset_index()

    # Remover colunas de épico com poucos valores > 0
    epic_cols = [col for col in version_data.columns if col.startswith('cod_epic_')]
    cols_to_drop = [col for col in epic_cols if version_data[col].gt(0).sum() < 2]
    version_data.drop(columns=cols_to_drop, inplace=True)

    return version_data
