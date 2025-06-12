from fastapi import FastAPI, Depends, HTTPException
from . import models, schemas, security, database
from sqlalchemy.orm import Session

app = FastAPI()

# Эндпоинт для логина
@app.post("/login")
async def login(form_data: schemas.LoginForm, db: Session = Depends(database.get_db)):
    # Проверка существования пользователя в базе данных
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    
    if user is None or not security.verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    # Создание токена
    access_token = security.create_access_token(data={"sub": user.username})
    
    return {"access_token": access_token, "token_type": "bearer"}
@app.get("/users/me")
async def read_users_me(current_user: models.User = Depends(dependencies.get_current_user)):
    return {"username": current_user.username, "id": current_user.id}
