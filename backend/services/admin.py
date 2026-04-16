from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from backend.models.user import User
from backend.models.transaction import Transaction
from backend.services.auth import get_password_hash, verify_password


def get_all_admins(db: Session) -> List[User]:
    """Get all admin users"""
    return db.query(User).filter(User.role == "admin").all()


def get_admin_by_id(db: Session, admin_id: str) -> Optional[User]:
    """Get a specific admin by ID"""
    return db.query(User).filter(
        (User.id == admin_id) & (User.role == "admin")
    ).first()


def get_admin_by_email(db: Session, email: str) -> Optional[User]:
    """Get admin by email"""
    return db.query(User).filter(
        (User.email == email) & (User.role == "admin")
    ).first()


def create_admin(db: Session, email: str, password: str) -> User:
    """Create a new admin user"""
    # Check if email already exists
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        return None
    
    # Create new admin
    hashed_password = get_password_hash(password)
    admin = User(
        email=email,
        hashed_password=hashed_password,
        role="admin",
        credits=0  # Admins don't use credits
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin


def update_admin(db: Session, admin_id: str, email: Optional[str] = None, password: Optional[str] = None) -> Optional[User]:
    """Update an admin's details"""
    admin = get_admin_by_id(db, admin_id)
    if not admin:
        return None
    
    if email:
        # Check if email is already taken by another user
        existing = db.query(User).filter(
            (User.email == email) & (User.id != admin_id)
        ).first()
        if existing:
            return None
        admin.email = email
    
    if password:
        admin.hashed_password = get_password_hash(password)
    
    db.commit()
    db.refresh(admin)
    return admin


def delete_admin(db: Session, admin_id: str) -> bool:
    """Delete an admin user"""
    admin = get_admin_by_id(db, admin_id)
    if not admin:
        return False
    
    db.delete(admin)
    db.commit()
    return True


def get_admin_stats(db: Session) -> dict:
    """Get admin dashboard statistics"""
    total_users = db.query(func.count(User.id)).filter(User.role == "user").scalar() or 0
    total_admins = db.query(func.count(User.id)).filter(User.role == "admin").scalar() or 0
    total_transactions = db.query(func.count(Transaction.id)).scalar() or 0
    total_credits_sold = db.query(func.sum(Transaction.amount)).filter(
        Transaction.type == "credit"
    ).scalar() or 0
    
    return {
        "total_users": total_users,
        "total_admins": total_admins,
        "total_credits_sold": total_credits_sold,
        "total_transactions": total_transactions,
        "recent_signups": db.query(func.count(User.id)).filter(User.role == "user").scalar() or 0,
    }
