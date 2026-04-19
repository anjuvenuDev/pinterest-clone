from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.middleware import resolve_user_from_header
from app.core.rate_limit import RateLimiter
from app.routers.creator_ingestion import router as creator_router
from app.routers.health import router as health_router
from app.routers.recipe_feed import router as feed_router
from app.routers.remix import router as remix_router
from app.routers.user_auth import router as auth_router
from app.services.container import workers

app = FastAPI(title=settings.app_name)
rate_limiter = RateLimiter(requests_per_minute=settings.rate_limit_per_minute)

cors_origins = [origin.strip() for origin in settings.cors_allow_origins.split(",") if origin.strip()]
if not cors_origins:
    cors_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def auth_middleware(request, call_next):
    user_id, token = resolve_user_from_header(request.headers.get("Authorization"))
    request.state.user_id = user_id
    request.state.auth_token = token
    return await call_next(request)


@app.middleware("http")
async def rate_limit_middleware(request, call_next):
    client_ip = request.client.host if request.client else "unknown"
    if not rate_limiter.allow(client_ip):
        return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})
    return await call_next(request)

app.include_router(health_router)
app.include_router(feed_router)
app.include_router(auth_router)
app.include_router(creator_router)
app.include_router(remix_router)


@app.on_event("startup")
async def on_startup() -> None:
    await workers.start()


@app.on_event("shutdown")
async def on_shutdown() -> None:
    await workers.stop()
