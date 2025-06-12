from pydantic import BaseModel

# Схема для создания пользователя
class UserCreate(BaseModel):
    username: str
    password: str

# Схема для отображения пользователя
class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True  # Вместо orm_mode используем from_attributes (для Pydantic v2)
