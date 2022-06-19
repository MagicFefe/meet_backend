from fastapi import FastAPI
from aioredis import from_url
from config import REDIS_DB_URL
from db.database import Database
from dependencies import get_session
from endpoints import user
from starlette.middleware import Middleware
from middleware.authorization_middleware import AuthorizationMiddleware

db = Database()
redis_db = from_url(REDIS_DB_URL)
app = FastAPI(
    middleware=[
        Middleware(AuthorizationMiddleware)
    ]
)
app.include_router(user.router)


@app.on_event("startup")
async def init():
    await db.init_tables()


@app.on_event("shutdown")
async def disconnect():
    await db.engine.dispose()

app.dependency_overrides[get_session] = db.get_session
