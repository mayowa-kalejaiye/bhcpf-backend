from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_facilities(lga: str = None, ward: str = None):
    # TODO: Implement facility search from database
    return {"facilities": []}
