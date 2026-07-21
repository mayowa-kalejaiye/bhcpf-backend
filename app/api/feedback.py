from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.database.supabase_client import supabase

router = APIRouter()

class FeedbackRequest(BaseModel):
    message: str
    lga: Optional[str] = None
    ward: Optional[str] = None
    facility_name: Optional[str] = None

@router.post(
    "/",
    summary="Submit Feedback or Report Issues",
    description="Allows citizens to report illegal charges for covered services or submit general feedback about the BHCPF program."
)
async def submit_feedback(request: FeedbackRequest):
    """
    Save a user feedback report to the database.
    - **message**: The user's feedback or report description.
    - **facility_name**: (Optional) The specific PHC they are reporting.
    - **lga**: (Optional) The LGA of the facility.
    - **ward**: (Optional) The Ward of the facility.
    """
    if not request.message:
        raise HTTPException(status_code=400, detail="Message is required")
        
    try:
        data = {
            "message": request.message,
            "lga": request.lga,
            "ward": request.ward,
            "facility_name": request.facility_name
        }
        
        result = supabase.table("feedback").insert(data).execute()
        return {"status": "success", "message": "Feedback submitted successfully", "data": result.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
