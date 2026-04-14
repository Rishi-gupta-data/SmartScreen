from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from backend.services.auth import SECRET_KEY, ALGORITHM
from backend.db.connection import get_db
from backend.services.auth import get_user_by_email

security = HTTPBearer()


def get_current_user(token=Depends(security), db: Session = Depends(get_db)):
    """Extract and verify JWT token, return user dict with id, email, role"""
    if token is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    email: str = payload.get("sub")
    user_id: str = payload.get("id")
    role: str = payload.get("role", "user")
    
    if email is None or user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    # Return user dict with all relevant info
    return {
        "id": user.id,
        "email": user.email,
        "role": user.role,
    }


def admin_only(current_user=Depends(get_current_user)):
    """Dependency to check if user has admin role"""
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=403, 
            detail="Admin access required"
        )
    return current_user
