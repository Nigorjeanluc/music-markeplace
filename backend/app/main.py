from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from app.core.config import settings
from app.api.v1.router import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS middleware - explicitly handle all responses including errors
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
        if request.url.path in ["/health", "/"]:
            return await call_next(request)
        response = await call_next(request)
        return response


app.add_middleware(HealthCheckMiddleware)


@app.get("/")
def read_root():
    return {
        "message": "Music Marketplace API",
        "version": settings.VERSION,
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


# Include API routers
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/api/v1/debug/routes")
def list_routes():
    """Debug endpoint to list all registered routes."""
    from fastapi.routing import APIRoute
    routes = []
    for route in app.routes:
        if isinstance(route, APIRoute):
            routes.append({
                "path": route.path,
                "methods": list(route.methods)
            })
    return {"routes": routes, "total": len(routes)}