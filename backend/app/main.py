from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import project, meeting, risk, resource, status

app = FastAPI(
    title="PMO Intelligence Platform",
    description="Production-ready FastAPI backend for PMO Intelligence Platform",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://localhost:5173", "http://127.0.0.1:8080", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(project.router)
app.include_router(meeting.router)
app.include_router(risk.router)
app.include_router(resource.router)
app.include_router(status.router)


@app.get("/")
async def root():
    return {"message": "PMO Intelligence Platform API", "version": "1.0.0"}


@app.get("/health")
async def health():
    return {"status": "healthy"}

