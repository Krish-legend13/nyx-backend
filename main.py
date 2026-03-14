from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
import requests

from database import Base, engine
import models
from routes import analytics, downloads, friends, labs, leaderboard, users

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Nyx Nexus - The Digital Realm API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for local fetch and Requestly testing
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(users.router, prefix="/api", tags=["Users"])
app.include_router(labs.router, prefix="/api", tags=["Labs"])
app.include_router(friends.router, prefix="/api", tags=["Friends"])
app.include_router(downloads.router, prefix="/api", tags=["Downloads"])
app.include_router(analytics.router, prefix="/api", tags=["Analytics"])
app.include_router(leaderboard.router, prefix="/api", tags=["Leaderboard"])


import os
from fastapi.staticfiles import StaticFiles

# Serve the frontend directory using StaticFiles
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend'))
if os.path.exists(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
# Mr Nova AI (Ollama Integration)
# -----------------------------
@app.post("/nova-ai")
async def nova_ai(request: Request):
    try:
        data = await request.json()
        message = data.get("message", "")

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "gemma:2b",
                "prompt": f"""
You are MR NOVA, the AI assistant of Nyx Nexus cybersecurity training platform.
Give clear short answers related to cybersecurity, SOC, CTF, networking and hacking labs.
User question: {message}
""",
                "stream": False,
                "options": {
                    "num_predict": 100,
                    "temperature": 0.3
                }
            }
        )

        result = response.json()

        return {
            "reply": result.get("response", "")
        }

    except Exception as e:
        print("Nova AI error:", e)
        return {
            "reply": ""
        }