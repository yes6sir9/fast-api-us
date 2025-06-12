# Заглушка, замените на реальную логику работы с PostgreSQL
from typing import Optional

class UserInDB:
    def __init__(self, username: str, hashed_password: str):
        self.username = username
        self.hashed_password = hashed_password

def get_user_from_db(username: str) -> Optional[UserInDB]:
    # В реальном приложении здесь будет запрос к PostgreSQL
    if username == "testuser":
        # Предполагаем, что пароль "password123" был хеширован
        return UserInDB(username="testuser", hashed_password="$2b$12$EXAMPLEHASHFORPASSWORD123")
    return None