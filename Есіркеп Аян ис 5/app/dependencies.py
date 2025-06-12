from fastapi import Depends, HTTPException
from . import security, database, models
from sqlalchemy.orm import Session

def get_current_user(token: str = Depends(security.oauth2_scheme), db: Session = Depends(database.SessionLocal)):
    username = security.verify_token(token)
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
