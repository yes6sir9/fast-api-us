from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import crud, models, schemas, utils
from .database import get_db

# Инициализация приложения FastAPI
app = FastAPI()

# Эндпоинт для корня
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}

# Эндпоинт для регистрации
@app.post("/register")
async def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return await crud.create_user(db=db, user=user)

# Эндпоинт для логина
@app.post("/login")
async def login(credentials: schemas.UserCreate, db: Session = Depends(get_db)):
    # Поиск пользователя по имени
    user = await crud.get_user_by_username(db, credentials.username)
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # Обновление пароля, если он не хеширован
    updated_user = await crud.update_password_if_needed(db, user)
    if updated_user:
        pass

    # Сравнение пароля с хешированным
    if not utils.verify_password(credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    return {"message": "Login successful!"}
