from aioredis import from_url
from dependency_injector import containers, providers
from config import MEET_DB_URL, ENCODING
from db.database import Database


class DbContainer(containers.DeclarativeContainer):
    db = providers.Singleton(
        Database
    )

    meet_db = providers.Resource(
        from_url,
        url=MEET_DB_URL,
        encoding=ENCODING
    )

    db_session = providers.Resource(
        db.provided.get_session()
    )
