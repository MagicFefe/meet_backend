from sqlalchemy.ext.asyncio import AsyncSession
from models.user.user_register import UserRegister
from db.enitites.user import User


class UserRepository:
    async def add_user(self, db_session: AsyncSession, new_user: UserRegister):
        async with db_session:
            db_user = from_user_register_to_user(new_user)
            db_session.add(db_user)
            await db_session.commit()


def from_user_register_to_user(user_register: UserRegister) -> User:
    user = User()
    user.name = user_register.name
    user.email = user_register.email
    user.city = user_register.city
    user.country = user_register.country
    user.password = user_register.password
    return user
