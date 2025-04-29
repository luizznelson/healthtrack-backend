```markdown
# HealthTrack Backend

API RESTful desenvolvida em **FastAPI** e **PostgreSQL** para suportar todas as funcionalidades do HealthTrack: gestão de usuários (pacientes e nutricionistas), questionários de triagem, cálculo de scores de risco nutricional, geração de relatórios e integração com frontend e outros serviços.

---

## 🚀 Visão Geral

O backend do HealthTrack é responsável por:

- **Autenticação e Autorização**  
  Cadastro, login, proteção de rotas e emissão de tokens JWT.  
- **Gestão de Usuários**  
  CRUD de pacientes e profissionais, perfis e permissões.  
- **Questionários Nutricionais**  
  Criação, edição e resposta de questionários pré-consulta.  
- **Cálculo de Score de Risco**  
  Lógica de negócios para atribuir pesos, gerar scores e manter histórico.  
- **Relatórios e Dashboards**  
  Endpoints para exportar dados e métricas do paciente ao nutricionista.  
- **Integrações**  
  Banco de dados, envio de e-mail, serviços externos de nutrição, cache e filas de tarefas.

---

## 📘 Funcionalidades

- **Users**  
  - `/auth/register` — cria contas de paciente e nutricionista  
  - `/auth/login` — autentica e retorna token JWT  
  - `/users/me` — retorna dados do usuário logado  
- **Questionnaires**  
  - `/questionnaires` — CRUD de questionários  
  - `/questionnaires/{id}/responses` — envio de respostas pelo paciente  
- **Scores**  
  - Cálculo automático de risco com base nas respostas  
  - Histórico de scores por paciente  
- **Reports**  
  - Geração de relatórios PDF/JSON para análise e exportação    

---

## 🏗️ Arquitetura

```
healthtrack-backend/
├── alembic/                   # Migrações de banco de dados
├── app/
│   ├── core/                  # Configurações, segurança e exceções
│   ├── crud/                  # Operações de acesso a dados
│   ├── database.py            # Conexão e retry com o DB
│   ├── main.py                # FastAPI app, CORS e routers
│   ├── models/                # Modelos ORM (User, Questionnaire, Score, etc.)
│   ├── routers/               # Endpoints organizados por domínio
│   ├── schemas/               # Schemas Pydantic de request/response
│   └── services/              # Lógica de negócio e integrações externas
├── scripts/                   # Scripts utilitários (seed_db, etc.)
├── tests/                     # Testes unitários e de integração
├── .env.example               # Template de variáveis de ambiente
├── Dockerfile                 # Imagem do backend
├── docker-compose.yml         # Orquestração com PostgreSQL (e Adminer/Redis)
├── requirements.txt           # Dependências Python
└── README.md                  # Este documento
```

---

## 🛠️ Tecnologias

- **Linguagem**: Python 3.10+  
- **Framework**: FastAPI  
- **ORM**: SQLAlchemy + Alembic  
- **Banco de dados**: PostgreSQL  
- **Autenticação**: JWT (python-jose), OAuth2  
- **Teste**: pytest  
- **Containerização**: Docker & Docker Compose  

---

## ⚙️ Instalação e Uso

### 1. Clone

```bash
git clone https://github.com/luizznelson/healthtrack-backend.git
cd healthtrack-backend
```

### 2. Configure variáveis de ambiente

```bash
cp .env.example .env
```

Edite `.env` com suas credenciais e chaves:

```dotenv
POSTGRES_USER=postgres
POSTGRES_PASSWORD=<DB_PASSWORD>
POSTGRES_DB=healthtrack

DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}
SECRET_KEY=<YOUR_SECRET_KEY>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### 3. Suba os containers

```bash
docker-compose up -d --build
```

- **db** (PostgreSQL) em `localhost:5433` → container `5432`  
- **backend** em `localhost:8000`  

### 4. Inicialize dados

```bash
docker-compose exec backend python scripts/seed_db.py
```

Cria conta admin:
- **email**: `admin@healthtrack.com`  
- **senha**: `admin123`  

---

## 🧪 Testes

```bash
docker-compose exec backend pytest --maxfail=1 --disable-warnings -q
```

---

## 📜 Documentação

- **Swagger UI**: `http://127.0.0.1:8000/docs`  
- **Redoc**: `http://127.0.0.1:8000/redoc`  

---

---

## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).  

---
```