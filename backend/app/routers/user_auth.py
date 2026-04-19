from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.middleware import require_authenticated_user
from app.models.domain import LoginRequest, LoginResponse, OnboardingQuizRequest, UserProfile
from app.services.container import get_auth_service

router = APIRouter(prefix="/api", tags=["user-auth"])


@router.post("/auth/login", response_model=LoginResponse)
async def login(payload: LoginRequest, service=Depends(get_auth_service)):
    token, profile = await service.login(email=payload.email)
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return LoginResponse(access_token=token, user=UserProfile(**profile))


@router.get("/users/me", response_model=UserProfile)
async def get_me(user_id: str = Depends(require_authenticated_user), service=Depends(get_auth_service)):
    profile = await service.get_profile(user_id=user_id)
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return UserProfile(**profile)


@router.post("/users/onboarding-quiz", response_model=UserProfile)
async def save_onboarding(
    payload: OnboardingQuizRequest,
    user_id: str = Depends(require_authenticated_user),
    service=Depends(get_auth_service),
):
    profile = await service.save_onboarding(user_id=user_id, payload=payload.model_dump())
    return UserProfile(**profile)
