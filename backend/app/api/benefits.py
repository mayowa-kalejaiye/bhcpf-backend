from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_benefits(service: str = None):
    # TODO: Implement benefit search
    return {"benefits": []}
