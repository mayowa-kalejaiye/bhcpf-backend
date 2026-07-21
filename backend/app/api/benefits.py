from fastapi import APIRouter, HTTPException
from typing import Optional
from app.database.supabase_client import supabase

router = APIRouter()

@router.get("/")
async def get_benefits(service: Optional[str] = None, category: Optional[str] = None):
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
