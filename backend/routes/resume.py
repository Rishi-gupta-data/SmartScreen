from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.db.connection import get_db
from backend.services import credit_service, parsing_service
from backend.schemas.parsing_schema import ResumeParseRequest, ResumeParseResponse
from backend.utils.deps import get_current_user

router = APIRouter(prefix="/resume", tags=["resume"])

RESUME_PARSE_CREDITS = 5


@router.post("/parse", response_model=ResumeParseResponse)
def parse_resume(
    request: ResumeParseRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Parse a resume and extract structured information.
    Costs 5 credits per parse.
    """
    try:
        # Check if user has enough credits
        balance = credit_service.check_balance(db, current_user["id"])
        if balance < RESUME_PARSE_CREDITS:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient credits. Required: {RESUME_PARSE_CREDITS}, Available: {balance}",
            )

        # Parse the resume
        parsed_data = parsing_service.parse_resume(request.resume_text)

        # Deduct credits
        credit_service.deduct_credits(db, current_user["id"], RESUME_PARSE_CREDITS)

        # Return response
        return ResumeParseResponse(
            name=parsed_data.get("name"),
            email=parsed_data.get("email"),
            phone=parsed_data.get("phone"),
            skills=parsed_data.get("skills", []),
            experience=parsed_data.get("experience", []),
            education=parsed_data.get("education", []),
            raw_text=parsed_data.get("raw_text"),
            credits_deducted=RESUME_PARSE_CREDITS,
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing resume: {str(e)}")
