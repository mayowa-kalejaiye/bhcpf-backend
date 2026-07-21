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

@router.post("/")
async def submit_feedback(request: FeedbackRequest):
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
