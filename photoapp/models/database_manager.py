from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    create_async_engine, 
    AsyncEngine, 
    async_sessionmaker, 
    AsyncSession,
)

from config.settings import settings

# TODO: More engine settings
class DatabaseManager:
    def __init__(
        self, 
        url: str, 
        echo: bool = False, 
        echo_pool: bool = False,
        pool_size: int = 5,
        max_overflow: int = 10
    ):
        self.engine: AsyncEngine = create_async_engine(
            url=url,
            echo=echo,
            echo_pool=echo_pool,
            max_overflow=max_overflow,
            pool_size=pool_size
        )
        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            # These are turned off for async engine
            autoflush=False,  
            autocommit=False,
            expire_on_commit=False,
        )

    async def dispose(self) -> None:
        await self.engine.dispose()

    # Yield type, Send type (None)
    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            # No need to close because of context manager
            yield session


database_manager = DatabaseManager(
    url=str(settings.db.url),
    echo=settings.db.echo, 
    echo_pool=settings.db.echo_pool,
    pool_size=settings.db.pool_size,
    max_overflow=settings.db.max_overflow
)