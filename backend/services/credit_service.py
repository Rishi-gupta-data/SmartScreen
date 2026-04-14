from sqlalchemy.orm import Session
from backend.models.user import User
from backend.models.transaction import Transaction


def _log_transaction(db: Session, user_id: str, type: str, amount: int, description: str | None = None):
    txn = Transaction(user_id=user_id, type=type, amount=int(amount), description=description)
    db.add(txn)


def add_credits(db: Session, user_id: str, amount: int) -> User:
    user = db.query(User).filter(User.id == user_id).with_for_update().first()
    if not user:
        raise ValueError("User not found")
    user.credits = (user.credits or 0) + int(amount)
    db.add(user)
    _log_transaction(db, user_id, "add", amount, description="credit top-up")
    db.commit()
    db.refresh(user)
    return user


def deduct_credits(db: Session, user_id: str, amount: int) -> User:
    user = db.query(User).filter(User.id == user_id).with_for_update().first()
    if not user:
        raise ValueError("User not found")
    if (user.credits or 0) < amount:
        raise ValueError("Insufficient credits")
    user.credits = user.credits - int(amount)
    db.add(user)
    _log_transaction(db, user_id, "deduct", amount, description="consumed for operation")
    db.commit()
    db.refresh(user)
    return user


def check_balance(db: Session, user_id: str) -> int:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("User not found")
    return user.credits or 0
