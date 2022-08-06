from sys import modules
from dependency_injector.wiring import Provide, inject
from fastapi import FastAPI
from db.database import Database
from di.application_container import ApplicationContainer
from endpoints.update import update
from endpoints.user import user
from endpoints.meet import meet
from endpoints.auth import auth
from middleware.authorization_middleware import AuthorizationMiddleware
from repositories.user_repository import UserRepository
from utils.saveable_list.saveable_list import SaveableList

app = FastAPI()

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(meet.router)
app.include_router(update.router)


@app.on_event("startup")
@inject
async def init(
        repository: UserRepository = Provide[ApplicationContainer.repository_container.user_repository],
        db: Database = Provide[ApplicationContainer.db_container.db],
        meet_authors_id_storage: SaveableList = Provide[ApplicationContainer.meet_authors_id_storage]
):
    meet_authors_id_storage.on_restore()
    app.add_middleware(AuthorizationMiddleware, repository=repository)
    await db.init_tables()


@app.on_event("shutdown")
@inject
async def disconnect(
        db: Database = Provide[ApplicationContainer.db_container.db],
        meet_authors_id_storage: SaveableList = Provide[ApplicationContainer.meet_authors_id_storage]
):
    meet_authors_id_storage.on_save()
    await db.engine.dispose()


container = ApplicationContainer()
container.wire(
    modules=[modules[__name__]],
    packages=["endpoints"]
)
