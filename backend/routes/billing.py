from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.db.connection import get_db
from backend.services import credit_service
from backend.schemas.request_schema import BuyCreditRequest, CreditsResponse, TransactionResponse
from backend.utils.deps import get_current_user
from backend.models.transaction import Transaction

router = APIRouter(prefix="/billing", tags=["billing"])


@router.get("/credits", response_model=CreditsResponse)
def get_credits(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get user's current credit balance and usage summary"""
    try:
        user_id = current_user["id"]
        balance = credit_service.check_balance(db, user_id)
        
        # Get transaction summary
        transactions = db.query(Transaction).filter(Transaction.user_id == user_id).all()
        
        total_used = sum(
            t.amount for t in transactions if t.type == "deduct"
        )
        total_purchased = sum(
            t.amount for t in transactions if t.type == "add"
        )
        
        return CreditsResponse(
            user_id=user_id,
            current_balance=balance,
            total_used=total_used,
            total_purchased=total_purchased,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/buy-credits", response_model=TransactionResponse)
def buy_credits(
    req: BuyCreditRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Buy credits for the user.
    
    In production, this endpoint would:
    1. Integrate with payment gateway (Razorpay/Stripe)
    2. Only add credits after payment confirmation
    3. Return a payment link
    
    For MVP, we simulate credit purchase.
    """
    try:
        if req.amount <= 0:
            raise HTTPException(status_code=400, detail="Amount must be positive")
        
        user_id = current_user["id"]
        
        # Add credits (in production, only after payment confirmation)
        user = credit_service.add_credits(db, user_id, req.amount)
        
        # Get the transaction that was just created
        transaction = db.query(Transaction).filter(
            Transaction.user_id == user_id,
            Transaction.type == "add"
        ).order_by(Transaction.created_at.desc()).first()
        
        return TransactionResponse(
            id=transaction.id,
            user_id=transaction.user_id,
            type=transaction.type,
            amount=transaction.amount,
            description=transaction.description,
            created_at=transaction.created_at.isoformat(),
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/transactions")
def get_transactions(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 50,
):
    """Get user's transaction history"""
    try:
        user_id = current_user["id"]
        transactions = (
            db.query(Transaction)
            .filter(Transaction.user_id == user_id)
            .order_by(Transaction.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

        transaction_list = [
            TransactionResponse(
                id=t.id,
                user_id=t.user_id,
                type=t.type,
                amount=t.amount,
                description=t.description,
                created_at=t.created_at.isoformat(),
            )
            for t in transactions
        ]

        return {
            "transactions": [t.model_dump() for t in transaction_list],
            "total": len(transaction_list),
            "skip": skip,
            "limit": limit,
        }

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))