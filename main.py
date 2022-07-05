from fastapi import FastAPI
from db.database import Database
from dependencies import get_session
from endpoints import user
from endpoints.meet import meetpoint
from starlette.middleware import Middleware
from middleware.authorization_middleware import AuthorizationMiddleware

db = Database()
app = FastAPI(
    middleware=[
        Middleware(AuthorizationMiddleware)
    ]
)
app.include_router(user.router)
app.include_router(meetpoint.router)


@app.on_event("startup")
async def init():
    await db.init_tables()


@app.on_event("shutdown")
async def disconnect():
    await db.engine.dispose()


app.dependency_overrides[get_session] = db.get_session
