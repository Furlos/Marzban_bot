# Marzban Telegram Control Plane

Python/FastAPI internal backend + Aiogram Telegram bot + external Marzban API.

**Portfolio status:** backend integration prototype. The internal API has authentication and tests; external Marzban, Telegram and Stars payments have **not** been end-to-end tested in production. Do not publish a public VPN management endpoint or accept live payments based only on unit tests.

## Architecture

```text
Telegram client -> Aiogram bot -> internal authenticated FastAPI -> Marzban API
```

The backend owns Marzban admin credentials. The Telegram bot talks to the backend with a shared internal token; it **must not** expose the backend admin credentials to end users.

## Local setup

Requirements: Docker Engine + Docker Compose, your own Marzban installation, your own Telegram bot token.

1. Copy `.env.example` to `.env` locally.
2. Set `MARZBAN_API_URL`, `API_TOKEN`, `BOT_TOKEN`.
3. Generate and set a long random `INTERNAL_API_KEY` (never commit it).
4. Run `docker compose up --build`.
5. Inspect `docker compose logs` before testing with real users.

The backend is accessible **only on 127.0.0.1:3000** on the Docker host and on the private Compose network. Its user endpoints require the `X-Internal-Token` header.

### API

- `GET /health`: public container health check (contains no user info).
- `GET /users/{user_id}`: retrieve a user.
- `POST /users/`: create a user; JSON with `username`, `expire_days`, `data_limit_gb`.
- `PUT /users/{user_id}`: extend/update quota; JSON with `expire_days` and/or `traffic_gb`.

All `/users` endpoints require `X-Internal-Token`. The upstream Marzban URL may end in `/api` or specify the origin directly.

### Run backend tests (no credentials needed)

```bash
cd backend
python -m pip install -r requirements.txt pytest
PYTHONPATH=. python -m pytest -q tests
```

CI tests route authentication, path parameters, validation, and a mocked integration. No live external Marzban calls occur in CI.

## Remaining production requirements

- Test full Telegram -> internal API -> real Marzban flow using test credentials.
- Validate user provisioning, subscriptions, expiry and traffic limits.
- Verify Stars invoice prices and ensure payment **idempotency and durable receipt tracking** before handling paying users. The current bot's payments are a prototype; it has no persistent payment ledger.
- Add monitoring, admin recovery and appropriate rate limiting for commercial use.
- Keep the API behind a firewall/reverse proxy if publishing beyond the local Docker host.

## Portfolio value

Demonstrates FastAPI, Aiogram, Pydantic, HTTPX, async requests, Docker Compose, service boundaries, authentication and CI tests. It is not represented as a production-ready billing platform.
