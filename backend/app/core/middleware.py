from __future__ import annotations

from typing import Optional

from fastapi import Depends, Header, HTTPException, status


TOKEN_MAP = {
    "demo-token": "demo-user",
    "creator-token": "creator-user",
}


def resolve_user_from_header(authorization: str | None) -> tuple[str, Optional[str]]:
    auth_header = authorization or ""
    token: Optional[str] = None
    if auth_header.lower().startswith("bearer "):
        token = auth_header.split(" ", 1)[1].strip()

    return TOKEN_MAP.get(token, "anonymous"), token


def get_current_user_id(authorization: str | None = Header(default=None)) -> str:
    user_id, _ = resolve_user_from_header(authorization)
    return user_id


def require_authenticated_user(user_id: str = Depends(get_current_user_id)) -> str:
    if user_id == "anonymous":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )
    return user_id
