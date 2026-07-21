from fastapi import APIRouter, HTTPException
from typing import Optional
from app.database.supabase_client import supabase

router = APIRouter()

@router.get(
    "/",
    summary="Get Health Facilities",
    description="Retrieve a list of BHCPF-accredited primary health care facilities. You can optionally filter the results by Local Government Area (LGA) or Ward."
)
async def get_facilities(
    lga: Optional[str] = None, 
    ward: Optional[str] = None
):
    """
    Fetch facilities from the Supabase database.
    - **lga**: (Optional) Filter by Local Government Area name (case-insensitive substring match).
    - **ward**: (Optional) Filter by Ward name (case-insensitive substring match).
    """
    try:
        query = supabase.table("facilities").select("*")
        
        if lga:
            query = query.ilike("lga", f"%{lga}%")
        if ward:
            query = query.ilike("ward", f"%{ward}%")
            
        result = query.execute()
        return {"facilities": result.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
