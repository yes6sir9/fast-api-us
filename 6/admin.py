from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models import User
from database import get_db
from dependencies import require_role

admin_router = APIRouter()

@admin_router.get("/admin/users")
def list_users(db: Session = Depends(get_db), current_user: User = Depends(require_role("admin"))):
    return db.query(User).all()
