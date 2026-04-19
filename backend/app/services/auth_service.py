from __future__ import annotations

from app.repositories.supabase_repo import SupabaseRepository


class AuthService:
    def __init__(self, repo: SupabaseRepository) -> None:
        self.repo = repo

    async def login(self, email: str) -> tuple[str, dict]:
        if "creator" in email:
            user_id = "creator-user"
            token = "creator-token"
        else:
            user_id = "demo-user"
            token = "demo-token"
        profile = self.repo.get_user(user_id)
        return token, profile

    async def get_profile(self, user_id: str) -> dict | None:
        return self.repo.get_user(user_id)

    async def save_onboarding(self, user_id: str, payload: dict) -> dict:
        return self.repo.save_onboarding(user_id=user_id, payload=payload)
