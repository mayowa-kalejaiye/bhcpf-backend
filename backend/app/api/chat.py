from fastapi import APIRouter

router = APIRouter()

@router.post("/")
async def chat_endpoint():
    # TODO: Implement intent extraction, retrieval, and LLM response
    return {"answer": "Not implemented yet"}
