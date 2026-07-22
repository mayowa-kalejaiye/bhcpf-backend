from fastapi import APIRouter, HTTPException
from typing import Optional
from pydantic import BaseModel
from app.services.ai_service import generate_chat_response

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    language: Optional[str] = "Auto"
    state: Optional[str] = None
    lga: Optional[str] = None
    ward: Optional[str] = None

@router.post(
    "/",
    summary="AI Chat Orchestrator",
    description="Ask a natural language question about BHCPF coverage. The AI will look up your location and the official policy rules to give a precise, localized answer."
)
async def chat_endpoint(request: ChatRequest):
    """
    Process a natural language query using the Gemini AI RAG pipeline.
    
    - **message**: The citizen's question (e.g., "Is malaria free?").
    - **language**: (Optional) The dialect or language to respond in. Defaults to 'Auto' (matches user's language).
    - **state**: (Optional) The user's State to help locate nearby clinics.
    - **lga**: (Optional) The user's LGA to help locate nearby clinics.
    - **ward**: (Optional) The user's Ward to help locate nearby clinics.
    """
    if not request.message:
        raise HTTPException(status_code=400, detail="Message is required")
        
    try:
        answer = await generate_chat_response(
            question=request.message,
            language=request.language,
            state=request.state,
            lga=request.lga, 
            ward=request.ward
        )
        return {
            "answer": answer,
            "language_used": request.language,
            "state_searched": request.state,
            "lga_searched": request.lga,
            "ward_searched": request.ward
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
