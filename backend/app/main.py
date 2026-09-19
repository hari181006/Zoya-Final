from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from .database import Base, engine
from .routers import auth, admin, support
from . import models

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Zoya Services API",
    version="3.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(support.router)


# index.html is in the GitHub repository root
PROJECT_ROOT = Path(__file__).resolve().parents[2]
FRONTEND = PROJECT_ROOT / "frontend" / "index.html"

@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/", include_in_schema=False)
def home():
    if FRONTEND.exists():
        return FileResponse(
            FRONTEND,
            media_type="text/html"
        )

    return {
        "message": "Zoya Services frontend not found"
    }
