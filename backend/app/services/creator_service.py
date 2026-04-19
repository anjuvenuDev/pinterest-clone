from __future__ import annotations

from urllib.parse import urlparse

from app.repositories.supabase_repo import SupabaseRepository
from app.services.external.search_client import SearchIndexClient
from app.services.external.storage_client import StorageClient
from app.services.worker_bus import WorkerBus


class CreatorService:
    def __init__(
        self,
        repo: SupabaseRepository,
        workers: WorkerBus,
        search_client: SearchIndexClient,
        storage_client: StorageClient,
    ) -> None:
        self.repo = repo
        self.workers = workers
        self.search_client = search_client
        self.storage_client = storage_client

    async def ingest(self, *, source_url: str, consent_accepted: bool, creator_notes: str | None, user_id: str) -> dict:
        if not consent_accepted:
            raise ValueError("Creator consent is required for ingestion")

        parsed = urlparse(source_url)
        hostname = parsed.netloc or "external"
        image = self.storage_client.persist_asset(source_url)
        title = creator_notes.strip() if creator_notes else f"Imported recipe from {hostname}"

        recipe = self.repo.create_recipe(
            image=image,
            title=title,
            source_url=source_url,
            creator_id=user_id,
            tags=["imported", "creator"],
        )

        await self.workers.enqueue("scraper_jobs", {"source_url": source_url, "recipe_id": recipe["id"]})
        await self.workers.enqueue("search_indexing", self.search_client.index_recipe(recipe["id"]))
        return recipe
