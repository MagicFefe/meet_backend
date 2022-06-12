import http

from fastapi import Depends, FastAPI
from db.database import Database
from models.user.user_register import UserRegister
from repositories.user_repository import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from deps import get_session

app = FastAPI()
db = Database()


@app.on_event("startup")
async def init():
    await db.init_tables()


@app.on_event("shutdown")
async def disconnect():
    await db.engine.dispose()


@app.post(path="/api/user", status_code=201, response_model=int)
async def create_user(user_register: UserRegister, session: AsyncSession = Depends(get_session)) -> int:
    repo = UserRepository()
    async with session.begin():
        await repo.add_user(session, user_register)
    return http.HTTPStatus.CREATED

app.dependency_overrides[get_session] = db.get_session
