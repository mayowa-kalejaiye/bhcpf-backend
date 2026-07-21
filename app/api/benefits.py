from fastapi import APIRouter, HTTPException
from typing import Optional
from app.database.supabase_client import supabase

router = APIRouter()

@router.get(
    "/",
    summary="Get BHCPF Benefit Rules",
    description="Retrieve the official list of healthcare services covered under the Basic Health Care Provision Fund (BHCPF)."
)
async def get_benefits(
    service: Optional[str] = None, 
    category: Optional[str] = None
):
    """
    Fetch benefit rules from the Supabase database.
    - **service**: (Optional) Filter by the name of the service (e.g., 'malaria').
    - **category**: (Optional) Filter by the broad category (e.g., 'Maternal', 'Child Health').
    """
    try:
        query = supabase.table("benefits").select("*")
        
        if service:
            query = query.ilike("service", f"%{service}%")
        if category:
            query = query.ilike("category", f"%{category}%")
            
        result = query.execute()
        return {"benefits": result.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
