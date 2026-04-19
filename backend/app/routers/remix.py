from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.middleware import require_authenticated_user
from app.models.domain import RemixRequest, RemixResponse
from app.services.container import get_remix_service

router = APIRouter(prefix="/api", tags=["remix"])


@router.post("/remix", response_model=RemixResponse)
async def remix_recipe(
    payload: RemixRequest,
    user_id: str = Depends(require_authenticated_user),
    service=Depends(get_remix_service),
):
    try:
        remix = await service.remix(
            recipe_id=payload.recipe_id,
            ingredient_swaps=payload.ingredient_swaps,
            goal=payload.goal,
            user_id=user_id,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    return RemixResponse(
        success=True,
        remix_id=remix["id"],
        base_recipe_id=remix["base_recipe_id"],
        remixed_title=remix["remixed_title"],
        ingredient_swaps=remix["ingredient_swaps"],
        ai_summary=remix["ai_summary"],
    )
