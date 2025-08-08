"""
AETHER API - FastAPI Backend
© 2024 AlgoRythm Tech - Built by Sri Aasrith Souri Kompella
"""

from fastapi import FastAPI, HTTPException, Depends, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import asyncio
import json
import uuid
from datetime import datetime
import logging
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.aether_engine import AETHEREngine, AETHERConfig, UserProfile

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AETHER API",
    description="Advanced Engine for Thought, Heuristic Emotion and Reasoning - Built by AlgoRythm Tech",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Initialize AETHER Engine
logger.info("Initializing AETHER Engine...")
aether_engine = AETHEREngine()

# Session management
sessions: Dict[str, Dict] = {}


# Pydantic models
class ChatRequest(BaseModel):
    message: str = Field(..., description="User's message to AETHER")
    session_id: Optional[str] = Field(None, description="Session ID for conversation continuity")
    user_id: Optional[str] = Field(None, description="User ID for personalization")
    stream: bool = Field(False, description="Enable streaming response")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Who built you?",
                "session_id": "uuid-here",
                "user_id": "user123",
                "stream": False
            }
        }


class CustomizationRequest(BaseModel):
    user_id: str = Field(..., description="User ID")
    personality: Optional[str] = Field(None, description="Personality preference")
    response_style: Optional[str] = Field(None, description="Response style preference")
    expertise_areas: Optional[List[str]] = Field(None, description="Areas of expertise")
    language_preference: Optional[str] = Field(None, description="Language style preference")
    custom_instructions: Optional[str] = Field(None, description="Custom instructions for AETHER")
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user123",
                "personality": "friendly and professional",
                "response_style": "concise but thorough",
                "expertise_areas": ["coding", "AI", "startups"],
                "language_preference": "technical but accessible",
                "custom_instructions": "Always provide examples when explaining concepts"
            }
        }


class ChatResponse(BaseModel):
    response: str
    session_id: str
    thought_process: Optional[Dict[str, Any]] = None
    confidence: float
    metadata: Dict[str, Any]
    timestamp: str


class AETHERInfo(BaseModel):
    name: str
    full_name: str
    version: str
    company: str
    ceo: str
    description: str
    capabilities: List[str]
    status: str


# API Endpoints

@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint with AETHER information"""
    return {
        "name": "AETHER API",
        "description": "Advanced Engine for Thought, Heuristic Emotion and Reasoning",
        "company": "AlgoRythm Tech",
        "ceo": "Sri Aasrith Souri Kompella",
        "message": "Welcome to AETHER - The first AI built by teens, for everyone!",
        "docs": "/docs"
    }


@app.get("/info", response_model=AETHERInfo)
async def get_aether_info():
    """Get information about AETHER"""
    info = aether_engine.get_info()
    return AETHERInfo(**info)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "engine_status": aether_engine.get_info()["status"]
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint for interacting with AETHER
    """
    try:
        # Generate or retrieve session ID
        session_id = request.session_id or str(uuid.uuid4())
        
        # Initialize session if new
        if session_id not in sessions:
            sessions[session_id] = {
                "created_at": datetime.now().isoformat(),
                "messages": [],
                "user_id": request.user_id
            }
        
        # Add message to session history
        sessions[session_id]["messages"].append({
            "role": "user",
            "content": request.message,
            "timestamp": datetime.now().isoformat()
        })
        
        # Process message through AETHER
        result = await aether_engine.think(request.message, request.user_id)
        
        # Add response to session history
        sessions[session_id]["messages"].append({
            "role": "assistant",
            "content": result["response"],
            "timestamp": datetime.now().isoformat()
        })
        
        # Prepare response
        response = ChatResponse(
            response=result["response"],
            session_id=session_id,
            thought_process=result.get("thought_process"),
            confidence=result.get("confidence", 0.85),
            metadata=result.get("metadata", {}),
            timestamp=datetime.now().isoformat()
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """
    Streaming chat endpoint for real-time responses
    """
    async def generate():
        try:
            session_id = request.session_id or str(uuid.uuid4())
            
            # Process message
            result = await aether_engine.think(request.message, request.user_id)
            response_text = result["response"]
            
            # Stream response word by word
            words = response_text.split()
            for i, word in enumerate(words):
                chunk = {
                    "token": word + " ",
                    "session_id": session_id,
                    "is_final": i == len(words) - 1
                }
                yield f"data: {json.dumps(chunk)}\n\n"
                await asyncio.sleep(0.05)  # Simulate streaming delay
            
            # Send final metadata
            final_chunk = {
                "session_id": session_id,
                "is_final": True,
                "metadata": result.get("metadata", {}),
                "confidence": result.get("confidence", 0.85)
            }
            yield f"data: {json.dumps(final_chunk)}\n\n"
            
        except Exception as e:
            error_chunk = {"error": str(e)}
            yield f"data: {json.dumps(error_chunk)}\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream"
    )


@app.post("/customize")
async def customize_aether(request: CustomizationRequest):
    """
    Customize AETHER for a specific user
    """
    try:
        customization = {
            "personality": request.personality,
            "response_style": request.response_style,
            "expertise_areas": request.expertise_areas,
            "language_preference": request.language_preference,
            "custom_instructions": request.custom_instructions
        }
        
        # Remove None values
        customization = {k: v for k, v in customization.items() if v is not None}
        
        # Apply customization
        aether_engine.customize(request.user_id, customization)
        
        return {
            "status": "success",
            "message": f"AETHER customized for user {request.user_id}",
            "customization": customization
        }
        
    except Exception as e:
        logger.error(f"Error in customize endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/session/{session_id}")
async def get_session(session_id: str):
    """Get session history"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return sessions[session_id]


@app.delete("/session/{session_id}")
async def clear_session(session_id: str):
    """Clear a specific session"""
    if session_id in sessions:
        del sessions[session_id]
        aether_engine.reset_conversation()
        return {"status": "success", "message": "Session cleared"}
    
    raise HTTPException(status_code=404, detail="Session not found")


@app.get("/users/{user_id}/profile")
async def get_user_profile(user_id: str):
    """Get user profile and preferences"""
    if user_id in aether_engine.user_profiles:
        profile = aether_engine.user_profiles[user_id]
        return {
            "user_id": profile.user_id,
            "personality_preference": profile.personality_preference,
            "response_style": profile.response_style,
            "expertise_areas": profile.expertise_areas,
            "language_preference": profile.language_preference,
            "custom_instructions": profile.custom_instructions,
            "created_at": profile.created_at.isoformat(),
            "last_updated": profile.last_updated.isoformat()
        }
    
    raise HTTPException(status_code=404, detail="User profile not found")


@app.post("/feedback")
async def submit_feedback(
    session_id: str,
    rating: int = Field(..., ge=1, le=5),
    feedback: Optional[str] = None
):
    """Submit feedback for a conversation"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    sessions[session_id]["feedback"] = {
        "rating": rating,
        "feedback": feedback,
        "timestamp": datetime.now().isoformat()
    }
    
    return {"status": "success", "message": "Thank you for your feedback!"}


@app.get("/stats")
async def get_stats():
    """Get AETHER usage statistics"""
    total_sessions = len(sessions)
    total_messages = sum(len(s["messages"]) for s in sessions.values())
    total_users = len(aether_engine.user_profiles)
    
    return {
        "total_sessions": total_sessions,
        "total_messages": total_messages,
        "total_users": total_users,
        "active_sessions": len([s for s in sessions.values() 
                               if datetime.now().timestamp() - 
                               datetime.fromisoformat(s["created_at"]).timestamp() < 3600]),
        "engine_info": aether_engine.get_info()
    }


@app.on_event("startup")
async def startup_event():
    """Startup event handler"""
    logger.info("=" * 60)
    logger.info("🚀 AETHER API Starting...")
    logger.info("🏢 AlgoRythm Tech - First fully teen-built startup")
    logger.info("👤 CEO: Sri Aasrith Souri Kompella")
    logger.info("🧠 Advanced Engine for Thought, Heuristic Emotion and Reasoning")
    logger.info("=" * 60)


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler"""
    logger.info("Saving AETHER state...")
    aether_engine.save_state("aether_state.json")
    logger.info("AETHER API shutting down...")


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.now().isoformat()
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc),
            "timestamp": datetime.now().isoformat()
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
