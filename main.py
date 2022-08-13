from logging.config import dictConfig
from sys import modules
from dependency_injector.wiring import Provide, inject
from fastapi import FastAPI
from db.database import Database
from di.application_container import ApplicationContainer
from endpoints.feedback import feedback
from endpoints.update import update
from endpoints.user import user
from endpoints.meet import meet
from endpoints.auth import auth
from request_checkers.authorization_middleware import AuthorizationMiddleware
from services.user.user_service import UserService
from utils.saveable_list.saveable_list import SaveableList


log_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(asctime)s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",

        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    },
    "loggers": {
        "foo-logger": {"handlers": ["default"], "level": "DEBUG"},
    },
}
dictConfig(log_config)

app = FastAPI(
    debug=True
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(meet.router)
app.include_router(update.router)
app.include_router(feedback.router)


@app.on_event("startup")
@inject
async def init(
        service: UserService = Provide[ApplicationContainer.service_container.user_service],
        db: Database = Provide[ApplicationContainer.db_container.db],
        meet_authors_id_storage: SaveableList = Provide[ApplicationContainer.meet_container.meet_authors_id_storage]
):
    meet_authors_id_storage.on_restore()
    app.add_middleware(AuthorizationMiddleware, service=service)
    await db.init_tables()


@app.on_event("shutdown")
@inject
async def disconnect(
        db: Database = Provide[ApplicationContainer.db_container.db],
        meet_authors_id_storage: SaveableList = Provide[ApplicationContainer.meet_container.meet_authors_id_storage]
):
    meet_authors_id_storage.on_save()
    await db.engine.dispose()


container = ApplicationContainer()
container.wire(
    modules=[modules[__name__]],
    packages=["endpoints"]
)
