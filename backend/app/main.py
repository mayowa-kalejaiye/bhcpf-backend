from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import chat, facilities, benefits, feedback

app = FastAPI(title="BHCPF Backend API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production to match your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(facilities.router, prefix="/api/facilities", tags=["Facilities"])
app.include_router(benefits.router, prefix="/api/benefits", tags=["Benefits"])
app.include_router(feedback.router, prefix="/api/feedback", tags=["Feedback"])

@app.get("/")
def read_root():
    return {"message": "Welcome to BHCPF API"}
