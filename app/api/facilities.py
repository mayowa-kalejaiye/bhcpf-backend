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
        
        # Dynamically generate Google Maps links for each facility
        facilities = result.data
        import urllib.parse
        for fac in facilities:
            query_string = f"{fac.get('facility_name', '')}, {fac.get('ward', '')} Ward, {fac.get('lga', '')} LGA, {fac.get('state', '')} State, Nigeria"
            encoded_query = urllib.parse.quote_plus(query_string)
            fac["google_maps_url"] = f"https://www.google.com/maps/search/?api=1&query={encoded_query}"
            
        return {"facilities": facilities}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
