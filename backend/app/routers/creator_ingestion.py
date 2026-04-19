from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.middleware import require_authenticated_user
from app.models.domain import CreatorIngestRequest, CreatorIngestResponse, Recipe
from app.services.container import get_creator_service

router = APIRouter(prefix="/api/creator", tags=["creator-ingestion"])


@router.post("/ingest", response_model=CreatorIngestResponse)
async def ingest_recipe(
    payload: CreatorIngestRequest,
    user_id: str = Depends(require_authenticated_user),
    service=Depends(get_creator_service),
):
    try:
        recipe = await service.ingest(
            source_url=str(payload.source_url),
            consent_accepted=payload.consent_accepted,
            creator_notes=payload.creator_notes,
            user_id=user_id,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return CreatorIngestResponse(
        success=True,
        recipe=Recipe(**recipe),
        message="Recipe imported and queued for scraping/indexing",
    )
