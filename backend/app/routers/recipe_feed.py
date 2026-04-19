from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.core.middleware import get_current_user_id, require_authenticated_user
from app.models.domain import ActionResponse, FeedResponse, Recipe
from app.services.container import get_feed_service

router = APIRouter(prefix="/api/feed", tags=["recipe-feed"])


@router.get("", response_model=FeedResponse)
async def get_feed(
    query: str | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    bookmarked: bool = Query(default=False),
    user_id: str = Depends(get_current_user_id),
    service=Depends(get_feed_service),
):
    if bookmarked:
        items = await service.get_bookmarks(user_id=user_id, limit=limit)
    else:
        items = await service.get_feed(query=query, limit=limit)
    return FeedResponse(items=[Recipe(**item) for item in items], total=len(items))


@router.get("/{recipe_id}", response_model=Recipe)
async def get_recipe(recipe_id: str, service=Depends(get_feed_service)):
    recipe = await service.get_recipe(recipe_id)
    if not recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    return Recipe(**recipe)


@router.post("/{recipe_id}/like", response_model=ActionResponse)
async def like_recipe(
    recipe_id: str,
    user_id: str = Depends(require_authenticated_user),
    service=Depends(get_feed_service),
):
    ok = await service.toggle_like(user_id=user_id, recipe_id=recipe_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    return ActionResponse(success=True, action="like", recipe_id=recipe_id)


@router.post("/{recipe_id}/bookmark", response_model=ActionResponse)
async def bookmark_recipe(
    recipe_id: str,
    user_id: str = Depends(require_authenticated_user),
    service=Depends(get_feed_service),
):
    ok = await service.toggle_bookmark(user_id=user_id, recipe_id=recipe_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    return ActionResponse(success=True, action="bookmark", recipe_id=recipe_id)
