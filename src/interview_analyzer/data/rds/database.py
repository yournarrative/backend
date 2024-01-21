from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from starlette.datastructures import State

from interview_analyzer.data.rds.model import create_extensions, Base, create_update_triggers, \
    create_users_trigger, create_interviews_trigger
from interview_analyzer.utils.standard_logger import get_logger


logger = get_logger()


class DatabaseAccessLayer:
    def __init__(self, host: str, port: str, name: str, user: str, password: str, protocol: str):
        self.database_url = f"{protocol}://{user}:{password}@{host}:{port}/{name}"
        logger.debug(f"Database URL: {self.database_url}")
        self.async_engine: AsyncEngine = create_async_engine(self.database_url, future=True)
        self.async_session: AsyncSession = sessionmaker(
            self.async_engine, expire_on_commit=False, class_=AsyncSession
        )()

    async def _init_db(self):
        async with self.async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await create_extensions(conn)
            await create_update_triggers(conn)
            await conn.run_sync(Base.metadata.create_all)
            await create_users_trigger(conn)
            await create_interviews_trigger(conn)

        sql_files = (
            "01-users-table-data-init",
            "02-interviews-table-data-init",
        )

        for file in sql_files:
            with open(f"resources/sql/{file}.sql") as f:
                sql_code = f.read()

                async with self.async_session as session:
                    try:
                        logger.info(f"Inserting data from file: {file}")
                        await session.execute(text(sql_code))
                        await session.commit()
                    except IntegrityError as e:
                        logger.info(e)

    async def _validate_connection(self):
        async with self.async_session as session:
            try:
                await session.execute(text("SELECT 1"))
                await session.commit()
                logger.debug(f"Successfully validated connection to database url {self.database_url}")
            except Exception as e:
                logger.error(f"Error validating connection to database url {self.database_url}: {e}")
                raise e


async def create_database_access_layer(state: State) -> DatabaseAccessLayer:
    logger.debug("Creating database access layer...")

    try:
        db = DatabaseAccessLayer(
            host=state.env.get("DB_HOST"),
            port=state.env.get("DB_PORT"),
            name=state.env.get("DB_NAME"),
            user=state.env.get("DB_USER"),
            password=state.env.get("DB_PASSWORD"),
            protocol=state.env.get("DB_PROTOCOL"),
        )
        if state.env.get("ENVIRONMENT") == "local":
            await db._init_db()
        await db._validate_connection()
    except Exception as e:
        logger.error(f"Error creating database access layer: {e}")
        raise e
    else:
        logger.debug("Database access layer created.")
        return db
