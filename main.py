from fastapi import FastAPI
from db.database import Database
from models.user.user_register import UserRegister
from repositories.user_repository import UserRepository

app = FastAPI()
db = Database()


@app.on_event("startup")
async def init():
    await db.init_tables()


@app.on_event("shutdown")
async def disconnect():
    await db.engine.dispose()


@app.post(path="/api/user", status_code=200)
async def create_user(user_register: UserRegister):
    repo = UserRepository()
    async with db.get_session() as session:
        await repo.add_user(session, user_register)
