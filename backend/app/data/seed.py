SEED_RECIPES = [
    {
        "id": "0",
        "image": "https://notjustdev-dummy.s3.us-east-2.amazonaws.com/pinterest/0.jpeg",
        "title": "Protein breakfast bowl",
        "source_url": "https://example.com/recipes/protein-bowl",
        "creator_id": "demo-user",
        "tags": ["breakfast", "high-protein"],
    },
    {
        "id": "1",
        "image": "https://notjustdev-dummy.s3.us-east-2.amazonaws.com/pinterest/1.jpeg",
        "title": "One-pot pasta",
        "source_url": "https://example.com/recipes/one-pot-pasta",
        "creator_id": "creator-user",
        "tags": ["dinner", "quick"],
    },
    {
        "id": "2",
        "image": "https://notjustdev-dummy.s3.us-east-2.amazonaws.com/pinterest/2.jpeg",
        "title": "Crispy tofu rice bowl",
        "source_url": "https://example.com/recipes/tofu-bowl",
        "creator_id": "creator-user",
        "tags": ["vegan", "meal-prep"],
    },
]

SEED_USERS = {
    "demo-user": {
        "id": "demo-user",
        "name": "Anjana",
        "email": "anjana@example.com",
        "roles": ["home-cook"],
        "onboarding_completed": False,
    },
    "creator-user": {
        "id": "creator-user",
        "name": "Recipe Creator",
        "email": "creator@example.com",
        "roles": ["creator"],
        "onboarding_completed": True,
    },
}
