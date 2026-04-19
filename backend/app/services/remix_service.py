from __future__ import annotations

from app.repositories.supabase_repo import SupabaseRepository
from app.services.external.llm_client import LLMClient
from app.services.worker_bus import WorkerBus


class RemixService:
    def __init__(self, repo: SupabaseRepository, llm_client: LLMClient, workers: WorkerBus) -> None:
        self.repo = repo
        self.llm_client = llm_client
        self.workers = workers

    async def remix(
        self,
        *,
        recipe_id: str,
        ingredient_swaps: dict,
        goal: str | None,
        user_id: str,
    ) -> dict:
        base_recipe = self.repo.get_recipe(recipe_id)
        if not base_recipe:
            raise ValueError("Base recipe not found")

        remixed_title, ai_summary = self.llm_client.generate_remix(
            title=base_recipe["title"],
            ingredient_swaps=ingredient_swaps,
            goal=goal or "",
        )

        remix = self.repo.save_remix(
            user_id=user_id,
            base_recipe_id=recipe_id,
            remixed_title=remixed_title,
            ingredient_swaps=ingredient_swaps,
            ai_summary=ai_summary,
        )
        await self.workers.enqueue("feed_ranking", {"reason": "new_remix", "remix_id": remix["id"]})
        return remix
