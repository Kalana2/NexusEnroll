from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    from src.database.connection import DatabaseManager
    from src.events.event_publisher import EventPublisher
    
    # Initialize database
    db_manager = DatabaseManager()
    print("✅ Database initialized")
    
    # Initialize event publisher
    EventPublisher.initialize()
    print("✅ Event Publisher initialized")
    print("🚀 User Service started successfully on port 8001")
    
    yield
    
    # Shutdown
    print("👋 User Service shutting down")

app = FastAPI(
    title="NexusEnroll User Service",
    description="Manages student, faculty, and admin accounts, roles, and states",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "user-service",
        "version": "1.0.0",
        "port": 8001
    }

# Include routes
from src.controllers.user_controller import router as user_router
app.include_router(user_router, prefix="/api/v1/users", tags=["users"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )