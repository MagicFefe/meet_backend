from fastapi import FastAPI
from db.database import Database
from dependencies import get_session
from endpoints.user import user
from endpoints.meet import meet
from starlette.middleware import Middleware
from middleware.authorization_middleware import AuthorizationMiddleware
from repositories.user_repository import UserRepository
from nest_asyncio import apply

apply()
db = Database()
app = FastAPI(
    middleware=[
        Middleware(AuthorizationMiddleware, db=db, repository=UserRepository())
    ]
)
app.include_router(user.router)
app.include_router(meet.router)


@app.on_event("startup")
async def init():
    await db.init_tables()


@app.on_event("shutdown")
async def disconnect():
    await db.engine.dispose()

app.dependency_overrides[get_session] = db.get_session
