from __future__ import annotations

from typing import Dict, List, Optional

from pydantic import BaseModel, Field, HttpUrl


class Recipe(BaseModel):
    id: str
    image: str
    title: str
    source_url: Optional[str] = None
    creator_id: str = "demo-user"
    tags: List[str] = Field(default_factory=list)


class FeedResponse(BaseModel):
    items: List[Recipe]
    total: int


class ActionResponse(BaseModel):
    success: bool
    action: str
    recipe_id: str


class LoginRequest(BaseModel):
    email: str


class UserProfile(BaseModel):
    id: str
    name: str
    email: str
    roles: List[str] = Field(default_factory=list)
    onboarding_completed: bool = False
    bookmarks: int = 0
    likes: int = 0


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserProfile


class OnboardingQuizRequest(BaseModel):
    roles: List[str] = Field(default_factory=list)
    quiz_answers: Dict[str, str] = Field(default_factory=dict)


class CreatorIngestRequest(BaseModel):
    source_url: HttpUrl
    consent_accepted: bool
    creator_notes: Optional[str] = None


class CreatorIngestResponse(BaseModel):
    success: bool
    recipe: Recipe
    message: str


class RemixRequest(BaseModel):
    recipe_id: str
    ingredient_swaps: Dict[str, str] = Field(default_factory=dict)
    goal: Optional[str] = None


class RemixResponse(BaseModel):
    success: bool
    remix_id: str
    base_recipe_id: str
    remixed_title: str
    ingredient_swaps: Dict[str, str]
    ai_summary: str


class HealthResponse(BaseModel):
    status: str
    components: Dict[str, object]
