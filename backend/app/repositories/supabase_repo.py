from __future__ import annotations

import itertools
from collections import defaultdict
from copy import deepcopy
from typing import Dict, List, Optional, Set

from app.data.seed import SEED_RECIPES, SEED_USERS


class SupabaseRepository:
    """
    Supabase-style repository contract.
    Uses in-memory storage by default, with method boundaries kept close
    to where Supabase/Postgres queries would live in production.
    """

    def __init__(self, supabase_url: str = "", service_key: str = "") -> None:
        self.supabase_url = supabase_url
        self.service_key = service_key
        self.storage_mode = "in-memory"

        self._recipes: List[dict] = deepcopy(SEED_RECIPES)
        self._users: Dict[str, dict] = deepcopy(SEED_USERS)
        self._bookmarks: Dict[str, Set[str]] = defaultdict(set)
        self._likes: Dict[str, Set[str]] = defaultdict(set)
        self._remixes: List[dict] = []
        self._onboarding: Dict[str, dict] = {}
        self._next_recipe_id = itertools.count(len(self._recipes))
        self._next_remix_id = itertools.count(1)

    def list_recipes(self, query: Optional[str] = None, limit: int = 20) -> List[dict]:
        items = self._recipes
        if query:
            q = query.lower().strip()
            items = [r for r in items if q in r["title"].lower() or q in " ".join(r.get("tags", [])).lower()]
        return items[:limit]

    def get_recipe(self, recipe_id: str) -> Optional[dict]:
        return next((r for r in self._recipes if r["id"] == recipe_id), None)

    def create_recipe(
        self,
        *,
        image: str,
        title: str,
        source_url: Optional[str],
        creator_id: str,
        tags: Optional[List[str]] = None,
    ) -> dict:
        recipe = {
            "id": str(next(self._next_recipe_id)),
            "image": image,
            "title": title,
            "source_url": source_url,
            "creator_id": creator_id,
            "tags": tags or [],
        }
        self._recipes.insert(0, recipe)
        return recipe

    def like_recipe(self, user_id: str, recipe_id: str) -> bool:
        if not self.get_recipe(recipe_id):
            return False
        if recipe_id in self._likes[user_id]:
            self._likes[user_id].remove(recipe_id)
        else:
            self._likes[user_id].add(recipe_id)
        return True

    def bookmark_recipe(self, user_id: str, recipe_id: str) -> bool:
        if not self.get_recipe(recipe_id):
            return False
        if recipe_id in self._bookmarks[user_id]:
            self._bookmarks[user_id].remove(recipe_id)
        else:
            self._bookmarks[user_id].add(recipe_id)
        return True

    def list_bookmarked_recipes(self, user_id: str, limit: int = 20) -> List[dict]:
        bookmarked_ids = self._bookmarks[user_id]
        items = [r for r in self._recipes if r["id"] in bookmarked_ids]
        return items[:limit]

    def get_user(self, user_id: str) -> Optional[dict]:
        user = self._users.get(user_id)
        if not user:
            return None

        payload = deepcopy(user)
        payload["bookmarks"] = len(self._bookmarks[user_id])
        payload["likes"] = len(self._likes[user_id])
        return payload

    def save_onboarding(self, user_id: str, payload: dict) -> dict:
        user = self._users.setdefault(
            user_id,
            {
                "id": user_id,
                "name": "New user",
                "email": f"{user_id}@example.com",
                "roles": [],
                "onboarding_completed": False,
            },
        )
        user["roles"] = payload.get("roles", [])
        user["onboarding_completed"] = True
        self._onboarding[user_id] = payload
        return user

    def save_remix(
        self,
        *,
        user_id: str,
        base_recipe_id: str,
        remixed_title: str,
        ingredient_swaps: dict,
        ai_summary: str,
    ) -> dict:
        remix = {
            "id": f"remix-{next(self._next_remix_id)}",
            "user_id": user_id,
            "base_recipe_id": base_recipe_id,
            "remixed_title": remixed_title,
            "ingredient_swaps": ingredient_swaps,
            "ai_summary": ai_summary,
        }
        self._remixes.append(remix)
        return remix
