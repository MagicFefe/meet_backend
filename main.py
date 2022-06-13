from fastapi import FastAPI
from db.database import Database
from dependencies import get_session
from endpoints import user

app = FastAPI()
app.include_router(user.router)
db = Database()


@app.on_event("startup")
async def init():
    await db.init_tables()


@app.on_event("shutdown")
async def disconnect():
    await db.engine.dispose()

app.dependency_overrides[get_session] = db.get_session
