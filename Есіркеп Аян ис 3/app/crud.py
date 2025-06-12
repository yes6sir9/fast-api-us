from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import models, schemas, utils

async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(models.User).filter(models.User.username == username))
    return result.scalar_one_or_none()

async def create_user(db: AsyncSession, user: schemas.UserCreate):
    db_user = models.User(username=user.username, password=user.password)
    db.add(db_user)
    await db.commit()  
    await db.refresh(db_user)  
    return db_user

async def update_password_if_needed(db: AsyncSession, user: models.User):
    if not user.password.startswith('$2b$'):
        hashed_password = utils.get_password_hash(user.password)  
        user.password = hashed_password  
        db.add(user)  
        await db.commit()  
        await db.refresh(user)  
        return user
    return None

async def verify_password(plain_password: str, hashed_password: str) -> bool:
    return utils.verify_password(plain_password, hashed_password)
