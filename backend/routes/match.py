from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.db.connection import get_db
from backend.services import credit_service, parsing_service
from backend.schemas.parsing_schema import MatchResponse
from backend.utils.deps import get_current_user
from pydantic import BaseModel

router = APIRouter(prefix="/match", tags=["match"])

MATCH_CREDITS = 5


class MatchRequestSimple(BaseModel):
    resume_text: str
    jd_text: str


@router.post("")  # ✅ Normalized: no trailing slash
def match_resume_to_jd(
    request: MatchRequestSimple,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Match a resume against a job description and generate recommendations.
    Costs 5 credits per match.
    """
    try:
        # Check credits
        balance = credit_service.check_balance(db, current_user["id"])
        if balance < MATCH_CREDITS:
            raise HTTPException(
                status_code=402,
                detail=f"Insufficient credits. Required: {MATCH_CREDITS}, Available: {balance}",
            )

        # Parse resume and JD
        resume_data = parsing_service.parse_resume(request.resume_text)
        jd_data = parsing_service.parse_jd(request.jd_text)

        # Perform matching
        match_result = parsing_service.match_resume_to_jd(resume_data, jd_data)

        # Deduct credits
        credit_service.deduct_credits(db, current_user["id"], MATCH_CREDITS)

        # Return response using actual keys from match_result
        return MatchResponse(
            match_score=match_result["match_score"],
            breakdown=match_result["breakdown"],
            skill_match=match_result["skill_match"],
            experience_match=match_result["experience_match"],
            education_match=match_result["education_match"],
            overall_recommendation=match_result["overall_recommendation"],
            recommendation_detail=match_result["recommendation_detail"],
            improvement_tips=match_result["improvement_tips"],
            credits_deducted=MATCH_CREDITS,
        )

    except HTTPException:
        raise
    except KeyError as e:
        raise HTTPException(status_code=500, detail=f"Unexpected match result format: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error matching resume to JD: {str(e)}")