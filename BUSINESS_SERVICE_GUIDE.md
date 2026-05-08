# Добавление бизнес-сервиса

## Принцип
- Gateway не реализует бизнес-логику: HTTP endpoint валидирует вход, берет авторизацию/access, вызывает downstream через RabbitMQ RPC и возвращает HTTP DTO.
- Стандартная цепочка: `src/domain/api/**` -> `src/domain/service/**` -> `src/infra/communication/**/repository.py` -> `broker.request(..., queue="...")`.
- HTTP DTO и RabbitMQ wire DTO разделены: `src/domain/models/**` для API, `src/infra/communication/**/models` или `schemas` для сообщений в backend-сервисы.
- Новый независимый backend-сервис оформляй отдельной папкой в `src/infra/communication/<service>/`; новую часть существующего server-сервиса добавляй в текущие `server` подпакеты.

## Порядок добавления
- Сначала зафиксируй контракт RabbitMQ: имя queue, request payload, success response, error response. Endpoint без backend consumer не проверить end-to-end.
- Добавь HTTP request/response модели в `src/domain/models/<service>/...`; не протаскивай сюда внутренние `*_id`, если API должен отдавать `*_url` или другой публичный формат.
- Добавь wire request/response модели в `src/infra/communication/<service>/models/...`; для нового сервиса заведи свой `ResponseMessage`, `ErrorResponse`, `StatusResponse` по образцу server/auth.
- Добавь repository, который получает `RabbitBroker` в `__init__`, собирает wire request, вызывает `await self.broker.request(request, queue="service.action")` и парсит `ResponseMessage[Success | ErrorResponse].model_validate_json(response.body)`.
- Добавь domain service, который вызывает repository, проверяет `isinstance(response.message, ErrorResponse)` и превращает downstream-ошибку в `ServiceException(response.status, response.message.message)`.
- Зарегистрируй repository и service в `src/dependency.py`: импортируй классы, добавь `get_<service>_repository`, `<Service>RepositoryDependency`, `get_<service>_service`, `<Service>ServiceDependency`.
- Добавь controller в `src/domain/api/<service>.py` или подпакет. По умолчанию используй `fastapi_controllers.Controller` и `Controller.create_router()`, как остальные controllers.
- Подключи router: top-level сервисы в `src/domain/api/__init__.py`, server-scoped фичи в `src/domain/api/server/__init__.py`.
- Запусти минимальную проверку: `uv run python -m compileall -q start.py src`.

## Endpoint Pattern
- Для endpoint с авторизацией используй `AuthorizedUserID` из `src/dependency.py`; в `Controller` его часто кладут в `__init__`, если он нужен всем методам controller.
- Для server-scoped endpoint сначала получи `access = await member_service.get_member_by_user(server_id, user_id)`, потом передавай `AccessData` в service/repository.
- В repository для server-scoped RPC вручную преобразуй `AccessData` в `AccessDataRequest` из wire-моделей.
- Для пагинации используй `PaginationDependency`; он дает `page` и `page_size` с дефолтами `1` и `50`.
- Для простого успешного ответа возвращай `StatusResponse()` из `src/domain/models/response.py`, не wire `StatusResponse`.

## Минимальный скелет
```python
# src/infra/communication/<service>/repository.py
class ExampleRepository:
    def __init__(self, broker: RabbitBroker):
        self.broker = broker

    async def create_item(self, name: str) -> ResponseMessage[ExampleResponse | ErrorResponse]:
        request = ExampleCreateRequest(name=name)
        response: RabbitMessage = await self.broker.request(
            request, queue="example.create"
        )
        return ResponseMessage[ExampleResponse | ErrorResponse].model_validate_json(
            response.body
        )
```

```python
# src/domain/service/<service>.py
class ExampleService:
    def __init__(self, repository: ExampleRepository) -> None:
        self.repository = repository

    async def create_item(self, name: str):
        response = await self.repository.create_item(name)
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message
```

```python
# src/domain/api/<service>.py
class ExampleController(Controller):
    prefix = "/example"
    tags = ["Example"]

    def __init__(self, user_id: AuthorizedUserID) -> None:
        self.user_id = user_id

    @post("/", response_model=ExampleResponse)
    async def create_item(self, body: ExampleCreateRequest, service: ExampleServiceDependency):
        return await service.create_item(body.name)
```

## Частые ошибки
- Не открывай RabbitMQ или Redis в route handler; все клиенты идут через DI и app state.
- Не смешивай `src/domain/models/**` и `src/infra/communication/**` модели в response_model endpoint.
- Не забывай экспортировать новые repository-классы из `repository/__init__.py`, если для сервиса используется пакет repository.
- Не добавляй S3/MinIO через `src/infra/s3` без починки: текущий модуль не подключен, ссылается на отсутствующий `env.minio` и отсутствующие зависимости.
- Не считай `uv.lock` источником Docker-зависимостей: Docker устанавливает только из `pyproject.toml`.
