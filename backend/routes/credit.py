from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.db.connection import get_db
from backend.services import credit_service
from backend.utils.deps import get_current_user, admin_only

router = APIRouter(prefix="/credits", tags=["credits"]) 


@router.get("")  # ✅ Normalized: no trailing slash
def get_credits(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        balance = credit_service.check_balance(db, current_user["id"])
        return {"user_id": current_user["id"], "credits": balance}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/add")
def add_credits(payload: dict, current_user=Depends(admin_only), db: Session = Depends(get_db)):
    """Add credits to user account. Admin only."""
    amount = payload.get("amount")
    if amount is None:
        raise HTTPException(status_code=400, detail="amount required")
    try:
        user = credit_service.add_credits(db, current_user["id"], int(amount))
        return {"user_id": user.id, "credits": user.credits}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/deduct")
def deduct_credits(payload: dict, current_user=Depends(admin_only), db: Session = Depends(get_db)):
    """Deduct credits from user account. Admin only (for testing)."""
    amount = payload.get("amount")
    if amount is None:
        raise HTTPException(status_code=400, detail="amount required")
    try:
        user = credit_service.deduct_credits(db, current_user["id"], int(amount))
        return {"user_id": user.id, "credits": user.credits}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
