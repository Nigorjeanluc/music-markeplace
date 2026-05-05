from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from pathlib import Path
from app.core.config import settings
from app.api.v1.router import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS middleware (still useful for development or if accessed from other origins)
cors_origins = settings.get_allowed_origins() if settings.get_allowed_origins() else ["*"]
allow_credentials = False if cors_origins == ["*"] else True

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


class HealthCheckMiddleware(BaseHTTPMiddleware):
    """Handle health checks before CORS middleware to avoid database dependency."""

    async def dispatch(self, request: Request, call_next):
        if request.url.path in ["/health"]:
            return await call_next(request)
        response = await call_next(request)
        return response


app.add_middleware(HealthCheckMiddleware)


@app.get("/health")
def health_check():
    return {"status": "healthy"}


# Include API routers
app.include_router(api_router, prefix=settings.API_V1_STR)


# Serve frontend static files
FRONTEND_DIST = Path(__file__).parent.parent.parent / "frontend" / "dist"

if FRONTEND_DIST.exists():
    # Serve static assets (js, css, images, etc.)
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIST / "assets"), name="assets")

    # Serve index.html for all other routes (SPA support)
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        index_file = FRONTEND_DIST / "index.html"
        if index_file.exists():
            return FileResponse(index_file)
        return {"message": "Music Marketplace API", "version": settings.VERSION, "docs": "/docs"}
else:
    @app.get("/")
    def read_root():
        return {
            "message": "Music Marketplace API",
            "version": settings.VERSION,
            "docs": "/docs",
            "note": "Frontend not built. Run 'cd frontend && npm run build'"
        }
