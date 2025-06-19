from sqlalchemy.orm import Session
from database import SessionLocal
from models import User

def promote_to_admin(email: str):
    db: Session = SessionLocal()
    user = db.query(User).filter(User.email == email).first()
    if user:
        user.role = "admin"
        db.commit()
        print(f"Пользователь {email} теперь admin")
    else:
        print("Пользователь не найден")

if __name__ == "__main__":
    promote_to_admin("admin@example.com")  # Заменить email при необходимости
