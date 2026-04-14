from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.db.connection import get_db
from backend.services import credit_service, parsing_service
from backend.schemas.parsing_schema import MatchRequest, MatchResponse
from backend.utils.deps import get_current_user

router = APIRouter(prefix="/match", tags=["match"])

MATCH_CREDITS = 5


@router.post("/", response_model=MatchResponse)
def match_resume_to_jd(
    request: MatchRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Match a resume against a job description and generate recommendations.
    Costs 5 credits per match.
    
    Requires parsed resume and JD data from /resume/parse and /jd/parse endpoints.
    """
    try:
        # Check if user has enough credits
        balance = credit_service.check_balance(db, current_user["id"])
        if balance < MATCH_CREDITS:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient credits. Required: {MATCH_CREDITS}, Available: {balance}",
            )

        # Validate input data
        if not request.resume_data or not request.jd_data:
            raise HTTPException(
                status_code=400,
                detail="Both resume_data and jd_data are required",
            )

        # Perform matching
        match_result = parsing_service.match_resume_to_jd(
            request.resume_data, request.jd_data
        )

        # Deduct credits
        credit_service.deduct_credits(db, current_user["id"], MATCH_CREDITS)

        # Return response
        return MatchResponse(
            match_score=match_result["match_score"],
            skill_match=match_result["skill_match"],
            experience_match=match_result["experience_match"],
            education_match=match_result["education_match"],
            overall_recommendation=match_result["overall_recommendation"],
            missing_skills=match_result["missing_skills"],
            bonus_skills=match_result["bonus_skills"],
            credits_deducted=MATCH_CREDITS,
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error matching resume to JD: {str(e)}")
