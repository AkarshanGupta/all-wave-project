from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import project, meeting, risk, resource, status
import os

app = FastAPI(
    title="PMO Intelligence Platform",
    description="Production-ready FastAPI backend for PMO Intelligence Platform",
    version="1.0.0",
)

# Configure CORS with environment-aware origins
allowed_origins = [
    "http://localhost:8080",
    "http://localhost:5173",
    "http://127.0.0.1:8080",
    "http://127.0.0.1:5173",
    "https://all-wave-project.onrender.com",
    "https://all-wave-project-ol5h.vercel.app",
]

# Add custom origins from environment if provided
env_origins = os.getenv("ALLOWED_ORIGINS", "")
if env_origins:
    allowed_origins.extend([origin.strip() for origin in env_origins.split(",") if origin.strip()])

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

app.include_router(project.router)
app.include_router(meeting.router)
app.include_router(risk.router)
app.include_router(resource.router)
app.include_router(status.router)


@app.get("/")
@app.head("/")
async def root():
    return {"message": "PMO Intelligence Platform API", "version": "1.0.0"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
