import os
import google.generativeai as genai
from typing import Optional, List, Dict
from app.database.supabase_client import supabase

# Initialize Gemini
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

def get_context(lga: Optional[str] = None, ward: Optional[str] = None) -> tuple[str, str]:
    # 1. Fetch Benefits Context
    benefits_response = supabase.table("benefits").select("*").execute()
    benefits_data = benefits_response.data
    
    benefits_context = "BHCPF Benefits Package:\n"
    for b in benefits_data:
        benefits_context += f"- Service: {b['service']} (Level: {b['level']}, Access: {b['access_point']})\n  Details: {b['details']}\n  Limits: {b['limits']}\n\n"
        
    # 2. Fetch Facilities Context
    facilities_context = ""
    if lga or ward:
        query = supabase.table("facilities").select("*")
        if lga:
            query = query.ilike("lga", f"%{lga}%")
        if ward:
            query = query.ilike("ward", f"%{ward}%")
        
        facilities_response = query.execute()
        facilities_data = facilities_response.data
        
        if facilities_data:
            facilities_context = "Available Facilities in requested area:\n"
            for f in facilities_data:
                facilities_context += f"- {f['facility_name']} (LGA: {f['lga']}, Ward: {f['ward']})\n"
        else:
            facilities_context = "No specific facilities found for the requested area. Please advise them to visit their registered PHC."
    else:
        facilities_context = "User did not specify a location. Ask them for their LGA or Ward if they want to know a specific facility."
        
    return benefits_context, facilities_context

async def generate_chat_response(question: str, lga: Optional[str] = None, ward: Optional[str] = None) -> str:
    benefits_context, facilities_context = get_context(lga, ward)
    
    prompt = f"""
You are the official BHCPF Access Assistant for Plateau State, Nigeria. 
Your job is to answer citizen questions about their health coverage and help them find facilities.

Be concise, helpful, and speak in plain English. 
Do not hallucinate. ONLY use the information provided in the context below. 
If a service is covered, state clearly whether it is at the Primary level (PHC) or Secondary level (General Hospital referral).
It is illegal for providers to charge for covered services. The hotline is 07007001111.

--- CONTEXT ---
{benefits_context}
{facilities_context}
---------------

User's Question: {question}
"""
    
    response = model.generate_content(prompt)
    return response.text
