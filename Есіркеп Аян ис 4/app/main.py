from fastapi import FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional

from app.schemas import UserLogin, Token
from app.security import create_access_token
from app.database import get_user_from_db # Из Задания 3, предполагается, что она возвращает хешированный пароль

# Для хеширования паролей, если еще не установлено: pip install bcrypt
from passlib.context import CryptContext

app = FastAPI()

# Контекст для хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Функция для верификации хеша пароля (из Задания 3)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

@app.post("/login", response_model=Token)
async def login_for_access_token(form_data: UserLogin): # Используем UserLogin для тела запроса
    user = get_user_from_db(form_data.username)

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user.username}
    )
    return {"access_token": access_token, "token_type": "bearer"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)