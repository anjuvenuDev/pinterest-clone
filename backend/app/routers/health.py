from __future__ import annotations

from fastapi import APIRouter, Depends

from app.models.domain import HealthResponse
from app.services.container import get_repo, get_workers

router = APIRouter(prefix="/api", tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check(repo=Depends(get_repo), workers=Depends(get_workers)):
    return HealthResponse(
        status="ok",
        components={
            "gateway": "up",
            "auth_middleware": "enabled",
            "rate_limiting": "enabled",
            "supabase": {"mode": repo.storage_mode},
            "workers": workers.snapshot(),
            "external_services": ["OpenAI/Claude", "Supabase Storage", "Typesense/Algolia", "Expo Push"],
        },
    )
