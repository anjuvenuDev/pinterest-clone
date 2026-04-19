from __future__ import annotations

from app.core.config import settings
from app.repositories.supabase_repo import SupabaseRepository
from app.services.auth_service import AuthService
from app.services.creator_service import CreatorService
from app.services.external.llm_client import LLMClient
from app.services.external.push_client import PushClient
from app.services.external.search_client import SearchIndexClient
from app.services.external.storage_client import StorageClient
from app.services.feed_service import FeedService
from app.services.remix_service import RemixService
from app.services.worker_bus import WorkerBus

repo = SupabaseRepository(
    supabase_url=settings.supabase_url,
    service_key=settings.supabase_service_role_key,
)
workers = WorkerBus()
llm_client = LLMClient()
push_client = PushClient()
search_client = SearchIndexClient()
storage_client = StorageClient()

feed_service = FeedService(repo=repo, workers=workers)
auth_service = AuthService(repo=repo)
creator_service = CreatorService(
    repo=repo,
    workers=workers,
    search_client=search_client,
    storage_client=storage_client,
)
remix_service = RemixService(repo=repo, llm_client=llm_client, workers=workers)


def get_repo() -> SupabaseRepository:
    return repo


def get_workers() -> WorkerBus:
    return workers


def get_feed_service() -> FeedService:
    return feed_service


def get_auth_service() -> AuthService:
    return auth_service


def get_creator_service() -> CreatorService:
    return creator_service


def get_remix_service() -> RemixService:
    return remix_service
