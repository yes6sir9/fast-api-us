from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import async_sessionmaker,create_async_engine,AsyncSession
DATABASE_URL = "postgresql+asyncpg://fastapitask:fastapitask@localhost:5432/fastapitask"

engine = create_async_engine(DATABASE_URL)

session_factory = async_sessionmaker(bind=engine,expire_on_commit=False,autoflush=False)

async def get_session():
    async with session_factory() as session:
        yield session

SessionDep = Annotated[AsyncSession,Depends(get_session)]

