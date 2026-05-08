# AGENTS.md

## Commands
- Use `uv sync` for local dependency setup; keep `uv.lock` updated when changing `pyproject.toml` dependencies.
- Run the service with `uv run python start.py`; Docker runs the same entrypoint through `entrypoint.sh`.
- Quick repo-local verification when no tests are added: `uv run python -m compileall -q start.py src`.
- There are currently no configured pytest, lint, format, typecheck, CI, pre-commit, or task-runner commands.
- Docker installs from `pyproject.toml` only (`COPY pyproject.toml`, then `uv pip install --system --editable .`), not from `uv.lock`.
- There is no `.dockerignore`; avoid leaving large local artifacts before Docker builds because `COPY . .` sends the full workspace.

## Runtime
- `start.py` serves `src.domain:app` with `reload=False`; app wiring is in `src/domain/main.py`.
- FastAPI docs are at `/api/docs`; OpenAPI is `/api/openapi.json`; HTTP routes are under `/api`, mainly `/api/auth` and `/api/server`.
- Runtime config comes from environment variables defined in `src/env_config.py`; no env file is configured.
- Supported env vars are `SERVER_HOST`, `SERVER_PORT`, `RABBITMQ_HOST`, `RABBITMQ_PORT`, `RABBITMQ_USER`, `RABBITMQ_PASSWORD`, `RABBITMQ_VHOST`, `RABBITMQ_REQUEST_TIMEOUT`, `REDIS_HOST`, `REDIS_PORT`, `REDIS_USER`, and `REDIS_PASSWORD`.
- Local defaults target RabbitMQ at `localhost:5672` (`guest`/`guest`, vhost `/`) and Redis at `localhost:6379`; integration work needs those services and backend consumers for the RPC queues.

## Architecture
- For adding a new business service or endpoint chain, follow `BUSINESS_SERVICE_GUIDE.md`.
- Dependency injection is centralized in `src/dependency.py`; add repository/service providers there instead of opening RabbitMQ or Redis clients inside route handlers.
- HTTP controllers live in `src/domain/api/**`; most use `fastapi_controllers.Controller.create_router()`, but `src/domain/api/server/member.py` is a plain `APIRouter`.
- Services in `src/domain/service/**` translate downstream `ErrorResponse` messages into `ServiceException`; repositories in `src/infra/communication/**/repository.py` perform RabbitMQ `broker.request(...)` calls.
- Keep HTTP DTOs in `src/domain/models/**` separate from RabbitMQ wire DTOs in `src/infra/communication/**/models` and `src/infra/communication/auth/schemas`.
- `RemapperService._fetch_file_urls()` currently returns static URLs under `https://static.demogram.ru/mixtura/`.
- Do not wire in `src/infra/s3` without fixing it first: it is unused, imports `..env_config`, references missing `env.minio`, and uses dependencies absent from `pyproject.toml`.
- `setup_logging()` writes rotating logs to `.local/temp.log`; `.local/` is gitignored.
