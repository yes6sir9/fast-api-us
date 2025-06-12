from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select,Result
from models import User
from database import SessionDep
from schemas import UserCreate, UserLogin
import uvicorn
app = FastAPI()


@app.post("/register")
async def register(user_in: UserCreate, session: SessionDep) -> UserLogin:
    stmt = select(User).where(User.username == user_in.username)
    result: Result = await session.execute(stmt)
    existing_user = result.scalar_one_or_none() 
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = User(**user_in.model_dump())
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user) 

    return new_user

@app.post("/login")
async def login(user_in: UserLogin, session:SessionDep) -> dict:
    db_user = select(User).where(User.username == user_in.username)
    result:Result = await session.execute(db_user)
    get_user = result.scalar_one_or_none()
    if not get_user or get_user.password != user_in.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return {"message": "Login successful"}

if __name__ == '__main__':
    uvicorn.run("main:app")