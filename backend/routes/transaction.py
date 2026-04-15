from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from backend.db.connection import get_db
from backend.models.transaction import Transaction
from backend.schemas.transaction_schema import TransactionListResponse, TransactionOut
from backend.utils.deps import get_current_user

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.get("", response_model=TransactionListResponse)  # ✅ Normalized: no trailing slash
def get_transactions(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    limit: int = Query(50, le=100, ge=1),
    offset: int = Query(0, ge=0),
    type_filter: str = Query(None, alias="type"),
):
    """
    Get transaction history for current user.
    
    Query Parameters:
    - limit: Number of transactions (default 50, max 100)
    - offset: Pagination offset (default 0)
    - type: Filter by transaction type (add, deduct, or null for all)
    
    Returns paginated list of transactions ordered by most recent first.
    """
    try:
        # Build query
        query = db.query(Transaction).filter(
            Transaction.user_id == current_user.id
        )

        # Apply type filter if provided
        if type_filter:
            query = query.filter(Transaction.type == type_filter)

        # Get total count
        total = query.count()

        # Apply pagination
        transactions = query.order_by(
            Transaction.created_at.desc()
        ).offset(offset).limit(limit).all()

        return TransactionListResponse(
            total=total,
            limit=limit,
            offset=offset,
            transactions=transactions,
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error fetching transactions: {str(e)}"
        )
