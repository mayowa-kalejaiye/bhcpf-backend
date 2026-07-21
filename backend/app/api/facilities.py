from fastapi import APIRouter, HTTPException
from typing import Optional
from app.database.supabase_client import supabase

router = APIRouter()

@router.get("/")
async def get_facilities(lga: Optional[str] = None, ward: Optional[str] = None):
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
