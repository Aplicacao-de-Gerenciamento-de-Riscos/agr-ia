# 🧠 Aplicação de IA - Gerenciamento de Riscos

Este repositório contém a aplicação de IA para o gerenciamento de riscos, desenvolvida em **Python** com **Flask** e **SQLAlchemy** para integração com o banco de dados.

---

## 📋 Pré-requisitos

Antes de rodar o projeto, você precisa ter os seguintes itens instalados:

- 🐍 **Python 3.12** - [Download aqui](https://www.python.org/downloads/)
- 🐘 **PostgreSQL** - [Guia de instalação](https://www.postgresql.org/download/)

### Instalando as Dependências

Para instalar as dependências do projeto, execute:

```bash
pip install -r requirements.txt
```

---

## 🛠️ Configuração do Banco de Dados

### 1. Criação do Banco de Dados PostgreSQL

Execute os seguintes comandos no PostgreSQL para criar o banco de dados e o usuário:

```sql
CREATE DATABASE agrbackend-dev;
CREATE USER usuario_ia WITH ENCRYPTED PASSWORD 'senha_ia';
GRANT ALL PRIVILEGES ON DATABASE agr_ia_db TO usuario_ia;
```

### 2. Configurar `database.py`

A configuração do banco de dados é feita no arquivo `database.py`. Edite esse arquivo para definir suas configurações de banco de dados PostgreSQL:

**Exemplo de `database.py`:**

```python
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:root@localhost:5432/agrbackend-dev")
```

---

## 🧩 Verificando o Modelo de IA

Certifique-se de que o arquivo do modelo de IA (por exemplo, `modelo_ia.joblib`) está incluído na pasta raiz do projeto ou na pasta especificada no código. 

Se o modelo estiver ausente, você precisará treinar o modelo novamente e salvar o arquivo `.joblib` no diretório correto.

---

## 🚀 Rodando a Aplicação Flask

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/Aplicacao-de-Gerenciamento-de-Riscos/agr-ia.git
   cd agr-ia
   ```

2. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure o banco de dados:**

   Certifique-se de que o banco de dados PostgreSQL está rodando e configurado corretamente no `database.py`.

4. **Execute a aplicação Flask:**

   ```bash
   flask run
   ```

   Por padrão, a aplicação estará disponível em:

   ```
   http://localhost:5000
   ```

---

## 📂 Estrutura do Projeto

```
agr-ia/
│-- app/
│   ├── __init__.py       # Inicialização da aplicação Flask
│   ├── routes.py         # Rotas da aplicação
│   ├── models.py         # Modelos de dados
│   └── services.py       # Lógica de IA e serviços
│-- database.py           # Configuração do banco de dados
│-- modelo_ia.pkl         # Arquivo do modelo de IA
│-- requirements.txt      # Dependências do projeto
└── README.md             # Documentação do projeto
```
