"""Main Application Entry Point"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import models
from app.database.connection import engine
from app.api import customers, vehicles, services
from app.agent.agent import BengelAIAgent

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="Bengkel AI Agent API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI Agent
ai_agent = BengelAIAgent()

# Include routers
app.include_router(customers.router)
app.include_router(vehicles.router)
app.include_router(services.router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Welcome to Bengkel AI Agent API"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/agent/chat")
async def chat(message: str):
    """Chat with AI Agent"""
    response = ai_agent.process_request(message)
    return {"response": response}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
