from __future__ import annotations


class SearchIndexClient:
    """Stub client for Typesense/Algolia indexing calls."""

    def index_recipe(self, recipe_id: str) -> dict:
        return {"queued": True, "recipe_id": recipe_id, "provider": "typesense/algolia"}
