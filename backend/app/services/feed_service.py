from __future__ import annotations

from typing import Optional

from app.repositories.supabase_repo import SupabaseRepository
from app.services.worker_bus import WorkerBus


class FeedService:
    def __init__(self, repo: SupabaseRepository, workers: WorkerBus) -> None:
        self.repo = repo
        self.workers = workers

    async def get_feed(self, query: Optional[str] = None, limit: int = 20) -> list[dict]:
        return self.repo.list_recipes(query=query, limit=limit)

    async def get_bookmarks(self, user_id: str, limit: int = 20) -> list[dict]:
        return self.repo.list_bookmarked_recipes(user_id=user_id, limit=limit)

    async def get_recipe(self, recipe_id: str) -> Optional[dict]:
        return self.repo.get_recipe(recipe_id)

    async def toggle_like(self, user_id: str, recipe_id: str) -> bool:
        ok = self.repo.like_recipe(user_id=user_id, recipe_id=recipe_id)
        if ok:
            await self.workers.enqueue("feed_ranking", {"recipe_id": recipe_id, "reason": "like"})
        return ok

    async def toggle_bookmark(self, user_id: str, recipe_id: str) -> bool:
        ok = self.repo.bookmark_recipe(user_id=user_id, recipe_id=recipe_id)
        if ok:
            await self.workers.enqueue("feed_ranking", {"recipe_id": recipe_id, "reason": "bookmark"})
        return ok
