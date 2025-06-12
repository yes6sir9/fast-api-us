from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Определяем базовый класс для декларативных моделей
Base = declarative_base()

class User(Base):
    __tablename__ = "users" # Имя таблицы в базе данных

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    def __repr__(self):
        return f"<User(username='{self.username}')>"