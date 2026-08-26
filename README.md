# 🏥 HealthCare API

API RESTful profissional para gerenciamento de clínicas médicas desenvolvida com **Django REST Framework**.

O projeto foi criado com foco em:

- aprendizado avançado backend
- arquitetura de software
- segurança de APIs
- processamento assíncrono
- integração entre microsserviços
- construção de portfólio profissional

---

# 🎯 Objetivo

Simular um sistema clínico real utilizado por:

- clínicas
- profissionais da saúde
- pacientes
- sistemas administrativos
- serviços externos

A proposta do projeto é demonstrar conhecimento em:

- modelagem de domínio
- arquitetura RESTful
- autenticação JWT
- RBAC
- integração entre APIs
- Docker
- Celery
- workflows assíncronos
- integração com IA

---

# 🧠 Arquitetura do Sistema

O sistema foi dividido em três camadas principais:

## 🏢 Camada Organizacional
- Clinic
- ClinicProfessional

Responsável pela gestão administrativa e vínculo entre clínica e profissional.

---

## 👤 Camada de Pessoas
- CustomUser
- Patient
- HealthcareProfessional

Responsável por autenticação, perfis e permissões.

---

## 🩺 Camada Clínica
- Appointment
- Consultation
- Prescription

Responsável por consultas, prontuário eletrônico e prescrições médicas.

---

# ⚙️ Stack Tecnológica

## Backend
- Python
- Django
- Django REST Framework

## Banco de Dados
- PostgreSQL
- Redis

## Infraestrutura
- Docker
- Docker Compose
- Celery
- Celery Beat

## Segurança
- JWT Authentication
- SimpleJWT
- RBAC
- Object Level Permissions

## Integrações
- Requests
- Google Gemini
- Medicines API

---

# 🌐 Integração com Medicines API

O projeto integra uma API externa de medicamentos desenvolvida separadamente.

Funcionalidades:

- bulário eletrônico
- consulta de medicamentos
- integração com IA
- tratamento de JSON
- consumo REST via `requests`

A integração permite utilizar medicamentos reais dentro das prescrições médicas.

---

# 📊 Módulo Core: Painel de Controle e Inteligência de Acesso (Dashboard)

Este módulo é o "cérebro" visual do **HealthCare**. Ele não apenas consolida os indicadores de desempenho da clínica e dos pacientes, mas também atua como a primeira camada de segurança comportamental do sistema, aplicando isolamento de dados dinâmico de acordo com o perfil de autenticação.

## 👥 Arquitetura de Perfis (RBAC)

O painel foi projetado sob o conceito de **Role-Based Access Control (Controle de Acesso Baseado em Papéis)**. A interface se transforma completamente dependendo da propriedade `role` do `CustomUsuario` logado:

### 1. Perfil: ADMINISTRADOR (`ADMIN`)
* **Foco:** Gestão macro, faturamento operacional e auditoria.
* **Métricas Exibidas:** Total geral de pacientes cadastrados no sistema, total de profissionais ativos e quantidade de clínicas integradas.
* **Fila de Atendimento:** Exibe o panorama completo de agendamentos de todas as unidades para o dia atual.

### 2. Perfil: PROFISSIONAL DE SAÚDE (`PROFISSIONAL`)
* **Foco:** Produtividade clínica e atendimento focado.
* **Métricas Exibidas:** Consultas agendadas para ele no dia, contador de pacientes únicos vinculados ao seu histórico e total de clínicas onde possui vínculo ativo.
* **Fila de Atendimento:** Exibe exclusivamente os pacientes agendados para o seu próprio CRM/Conselho no dia atual.

### 3. Perfil: PACIENTE (`PACIENTE`)
* **Foco:** Autoatendimento e transparência.
* **Métricas Exibidas:** Contador de consultas futuras marcadas.
* **Fila de Atendimento:** Uma visão cronológica de seus próximos compromissos (Data, Hora, Médico e Local), omitindo qualquer dado de terceiros.

---

## 🔒 Segurança de Nível de Linha (Row-Level Security) vs IDOR

Um erro comum em sistemas web é esconder elementos no HTML usando `{% if %}`, mas deixar o Back-end vulnerável a ataques de manipulação de URL (Insecure Direct Object Reference - IDOR), onde um usuário altera o ID numérico da rota (ex: `/agendamento/2/`) para ver dados alheios.

Para blindar o HealthCare, implementamos a **sobreposição do método `get_queryset()`** em todas as Views estruturais:

```python
def get_queryset(self):
    user = self.request.user
    queryset = super().get_queryset()
    
    if user.role == 'PACIENTE':
        return queryset.filter(patient__user=user)
    elif user.role == 'PROFISSIONAL':
        return queryset.filter(professional__user=user)
    return queryset # Admin visualiza o escopo total
```

# ⚡ Processamento Assíncrono

O projeto utiliza arquitetura distribuída com:

- Redis
- Celery Worker
- Celery Beat

## Casos Assíncronos

- envio de email para as clinicas cadastradas
- geração de PDFs
---

## 🚀 Arquitetura de Contêineres

A aplicação foi dividida em microserviços isolados para garantir performance e escalabilidade, seguindo a filosofia de um processo por contêiner:

* **`clinics_api_web`**: Aplicação Django (API principal).
* **`clinics_api_db`**: Banco de dados PostgreSQL (persistência de dados).
* **`redis`**: Banco em memória utilizado como Message Broker (intermediário) para o Celery.
* **`celery_worker`**: Processo responsável por escutar a fila do Redis e executar as tarefas pesadas (como disparo de e-mails) em segundo plano.
* **`celery_beat`**: Agendador de tarefas que dispara gatilhos em períodos programados.

---

## 🛠️ Pré-requisitos

Antes de iniciar, certifique-se de ter instalado em sua máquina:
* [Docker](https://docker.com)
* [Docker Compose](https://docker.com)

---

## 📦 Como Executar o Projeto

### 1. Configurar Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto com as suas credenciais. Para o correto funcionamento com o Docker, a URL do Redis deve apontar para o nome do serviço:

```env
# Banco de Dados
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=clinics_api
DB_HOST=clinics_api_db

# Celery / Redis Broker (Crucial para comunicação interna no Docker)
CELERY_BROKER_URL=redis://redis:6379/0
```

### 2. Construir e Iniciar os Serviços
Execute o comando abaixo para construir as imagens e iniciar todos os contêineres em segundo plano:

```bash
docker compose up -d --build
```
*O contêiner do Django possui um mecanismo automático que aguarda o banco PostgreSQL estabilizar para aplicar as migrações (`python manage.py migrate`) antes de iniciar o servidor.*

### 3. Criar um Superusuário (Admin)
Para acessar o painel administrativo do Django através do ambiente dockerizado, execute o comando interativo:

```bash
docker compose exec -it clinics_api_web python manage.py createsuperuser
```

---

## 📧 Distribuição e Agendamento de E-mails (Celery & Beat)

Para evitar que o usuário final sofra com lentidão ao esperar o disparo de e-mails (como confirmações de consultas ou alertas), o projeto utiliza processamento assíncrono.

### Como funciona o fluxo:
1. **Disparo Assíncrono (Worker):** Quando uma ação exige o envio de um e-mail, o Django publica a tarefa no **Redis** e responde imediatamente ao usuário. O `celery_worker` captura essa mensagem na fila e processa o envio em background.
2. **Agendamento (Beat):** Tarefas recorrentes (ex: relatórios diários de clínicas ou lembretes de consultas) são gerenciadas pelo `celery_beat` utilizando o scheduler `django_celery_beat`. Ele envia os gatilhos para o Redis nos horários programados.

### Comandos Úteis de Monitoramento

* **Visualizar logs de envio de e-mails do Worker:**
  ```bash
  docker compose logs -f celery_worker
  ```

* **Visualizar logs do Agendador (Beat):**
  ```bash
  docker compose logs -f celery_beat
  ```

* **Parar e limpar o ambiente Docker:**
  ```bash
  docker compose down
  ```

---
Desenvolvido para gerenciamento eficiente de clínicas médicas de forma escalável. 🩺

👨‍💻 Autor

Vitor Carvalho
Backend Developer — Python | Django | DRF
