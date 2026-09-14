"""Cognito settings loaded from environment."""

from __future__ import annotations

import os

from dotenv import load_dotenv
from pydantic import BaseModel, Field


class CognitoConfig(BaseModel):
    """AWS Cognito pool / client settings."""

    user_pool_id: str = Field(..., min_length=1)
    user_pool_client_id: str = Field(..., min_length=1)
    region: str = Field(..., min_length=1)
    identity_pool_id: str | None = None

    @classmethod
    def from_env(cls) -> CognitoConfig:
        """Load Cognito settings from `.env` / process environment."""
        load_dotenv()
        missing = [
            name
            for name in (
                "COGNITO_USER_POOL_ID",
                "COGNITO_USER_POOL_CLIENT_ID",
                "COGNITO_REGION",
            )
            if not os.getenv(name)
        ]
        if missing:
            raise ValueError(f"Missing required env vars: {', '.join(missing)}")
        return cls(
            user_pool_id=os.environ["COGNITO_USER_POOL_ID"],
            user_pool_client_id=os.environ["COGNITO_USER_POOL_CLIENT_ID"],
            region=os.environ["COGNITO_REGION"],
            identity_pool_id=os.getenv("COGNITO_IDENTITY_POOL_ID") or None,
        )
