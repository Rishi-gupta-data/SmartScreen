from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.db.connection import get_db
from backend.services import credit_service, parsing_service
from backend.schemas.parsing_schema import JDParseRequest, JDParseResponse
from backend.utils.deps import get_current_user

router = APIRouter(prefix="/jd", tags=["jd"])

JD_PARSE_CREDITS = 3


@router.post("/parse", response_model=JDParseResponse)
def parse_jd(
    request: JDParseRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Parse a job description and extract structured information.
    Costs 3 credits per parse.
    """
    try:
        # Check if user has enough credits
        balance = credit_service.check_balance(db, current_user["id"])
        if balance < JD_PARSE_CREDITS:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient credits. Required: {JD_PARSE_CREDITS}, Available: {balance}",
            )

        # Parse the JD
        parsed_data = parsing_service.parse_jd(request.jd_text)

        # Deduct credits
        credit_service.deduct_credits(db, current_user["id"], JD_PARSE_CREDITS)

        # Return response
        return JDParseResponse(
            title=parsed_data.get("title"),
            company=parsed_data.get("company"),
            required_skills=parsed_data.get("required_skills", []),
            preferred_skills=parsed_data.get("preferred_skills", []),
            experience_required=parsed_data.get("experience_required"),
            salary_range=parsed_data.get("salary_range"),
            qualifications=parsed_data.get("qualifications", []),
            responsibilities=parsed_data.get("responsibilities", []),
            raw_text=parsed_data.get("raw_text"),
            credits_deducted=JD_PARSE_CREDITS,
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing JD: {str(e)}")
