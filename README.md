# Marzban Telegram Control Plane

<p align="center">
  <b>A containerized Python backend + Telegram interface for managing Marzban users.</b>
</p>

<p align="center">
  <code>Python</code> · <code>FastAPI</code> · <code>Aiogram</code> · <code>HTTPX</code> · <code>Pydantic</code> · <code>Docker Compose</code>
</p>

---

## Why this project exists

The project separates a Telegram-facing interface from the infrastructure integration behind it. Instead of letting bot handlers talk directly to Marzban, requests go through a dedicated **FastAPI backend** responsible for user-management operations and communication with the external Marzban API.

That gives the project a simple service boundary and keeps Telegram-specific code independent from backend integration logic.

## Architecture

```text
┌──────────────────┐
│ Telegram user    │
└────────┬─────────┘
         │ command / interaction
         ▼
┌──────────────────┐
│ Telegram Bot     │
│ Aiogram + aiohttp│
└────────┬─────────┘
         │ HTTP
         ▼
┌──────────────────────────┐
│ Python Backend           │
│ FastAPI + Pydantic       │
│                          │
│ /users                   │
│  POST  create user       │
│  GET   get user          │
│  PUT   update user       │
└────────────┬─────────────┘
             │ async HTTP
             ▼
┌──────────────────────────┐
│ Marzban API              │
│ user / subscription data │
└──────────────────────────┘
```

Docker Compose connects both Python services on an internal network. The bot reaches the backend as `http://backend:3000`, while the backend receives Marzban credentials through environment variables.

## Backend design

The backend is intentionally split by responsibility:

```text
backend/src/
├── main.py          # FastAPI application entry point
├── api.py           # HTTP routes / transport layer
├── schemas.py       # Pydantic request models
├── user_service.py  # Marzban integration and user operations
└── config.py        # environment-based configuration
```

The `/users` API exposes create, read and update operations. Route handlers validate incoming data with Pydantic and delegate external API work to `UserService` rather than embedding integration logic into the HTTP layer.

## Service layout

```text
Marzban_bot/
├── backend/
│   ├── src/
│   ├── Dockerfile
│   ├── pyproject.toml
│   └── uv.lock
│
├── telegram_bot/
│   ├── src/
│   ├── Dockerfile
│   ├── pyproject.toml
│   └── uv.lock
│
└── docker-compose.yml
```

Both components are independently packaged Python services with their own dependency definitions and Dockerfiles.

## Tech stack

| Area | Technology | Role |
|---|---|---|
| Backend | Python 3.12+ | service and integration logic |
| API | FastAPI | HTTP boundary between bot and backend |
| Validation | Pydantic | request schemas |
| External I/O | HTTPX | async Marzban API communication |
| Telegram | Aiogram 3 | bot interface |
| Bot networking | aiohttp | backend communication |
| Runtime | Uvicorn | ASGI server |
| Packaging | uv | dependency locking |
| Deployment | Docker / Compose | multi-service environment |

## API surface

```http
POST /users/
GET  /users/{user_id}
PUT  /users/{user_id}
```

The API is responsible for translating application-level user operations into calls to Marzban.

## Run with Docker Compose

### 1. Clone

```bash
git clone https://github.com/Furlos/Marzban_bot.git
cd Marzban_bot
```

### 2. Configure credentials

Before running, provide your own values for:

```text
API_TOKEN=<marzban-admin-token>
API_URL=<marzban-api-url>
BOT_TOKEN=<telegram-bot-token>
```

The repository's Compose file contains placeholder values — do not commit real credentials.

### 3. Start both services

```bash
docker compose up --build
```

The backend is exposed on port `3000`; the Telegram container communicates with it through the Compose service network.

## Engineering ideas demonstrated

- separation between **transport**, **service** and **external integration** layers;
- asynchronous API communication;
- schema-based request validation;
- independently containerized Python services;
- service-to-service networking with Docker Compose;
- environment-driven external API configuration;
- Telegram as a client of a backend service rather than the location of all business logic.

## Current scope

This is a compact backend/integration project rather than a finished production platform. Useful next engineering steps would be automated tests, structured logging, health checks, stronger error mapping for upstream API failures and CI.

---

<p align="center">
  <b>Backend first:</b> Telegram is the interface; the Python service owns the integration boundary.
</p>
