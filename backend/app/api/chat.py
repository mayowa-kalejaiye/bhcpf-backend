from fastapi import APIRouter, HTTPException
from typing import Optional
from pydantic import BaseModel
from app.services.ai_service import generate_chat_response

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    lga: Optional[str] = None
    ward: Optional[str] = None

@router.post("/")
async def chat_endpoint(request: ChatRequest):
    if not request.message:
        raise HTTPException(status_code=400, detail="Message is required")
        
    try:
        answer = await generate_chat_response(
            question=request.message, 
            lga=request.lga, 
            ward=request.ward
        )
        return {
            "answer": answer,
            "lga_searched": request.lga,
            "ward_searched": request.ward
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
