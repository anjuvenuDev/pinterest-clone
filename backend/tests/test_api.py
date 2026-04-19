import pytest

from app.routers.health import health_check
from app.services.container import (
    auth_service,
    creator_service,
    feed_service,
    remix_service,
    repo,
    workers,
)


@pytest.mark.anyio
async def test_health_snapshot_contains_gateway_components():
    payload = await health_check(repo=repo, workers=workers)
    assert payload.status == "ok"
    assert payload.components["gateway"] == "up"
    assert "workers" in payload.components


@pytest.mark.anyio
async def test_feed_returns_seed_items():
    items = await feed_service.get_feed(limit=10)
    assert len(items) >= 1
    assert items[0]["id"] is not None


@pytest.mark.anyio
async def test_creator_ingestion_requires_consent():
    with pytest.raises(ValueError, match="consent"):
        await creator_service.ingest(
            source_url="https://example.com/recipe/no-consent",
            consent_accepted=False,
            creator_notes="No Consent",
            user_id="demo-user",
        )


@pytest.mark.anyio
async def test_creator_ingestion_success_and_feed_reflects_import():
    created = await creator_service.ingest(
        source_url="https://example.com/recipe/imported",
        consent_accepted=True,
        creator_notes="Imported Curry",
        user_id="demo-user",
    )
    items = await feed_service.get_feed(limit=20)
    ids = [item["id"] for item in items]
    assert created["id"] in ids


@pytest.mark.anyio
async def test_auth_profile_and_onboarding():
    token, profile = await auth_service.login("anjana@example.com")
    assert token == "demo-token"
    assert profile["id"] == "demo-user"

    updated = await auth_service.save_onboarding(
        "demo-user",
        {"roles": ["creator"], "quiz_answers": {"cuisine": "south-indian"}},
    )
    assert updated["onboarding_completed"] is True
    assert "creator" in updated["roles"]


@pytest.mark.anyio
async def test_remix_flow_and_worker_enqueue():
    base_recipe = (await feed_service.get_feed(limit=1))[0]
    before = workers.snapshot()["processed"].get("feed_ranking", 0)

    remix = await remix_service.remix(
        recipe_id=base_recipe["id"],
        ingredient_swaps={"butter": "olive oil"},
        goal="lower saturated fat",
        user_id="demo-user",
    )
    after = workers.snapshot()["processed"].get("feed_ranking", 0)

    assert remix["base_recipe_id"] == base_recipe["id"]
    assert remix["ingredient_swaps"]["butter"] == "olive oil"
    assert after == before + 1
