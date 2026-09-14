"""Tokens returned by Cognito USER_PASSWORD_AUTH."""

from pydantic import BaseModel, Field


class CognitoTokens(BaseModel):
    """JWT tokens from a successful Cognito login."""

    id_token: str = Field(..., min_length=1)
    access_token: str = Field(..., min_length=1)
    refresh_token: str | None = None
    expires_in: int | None = None
    token_type: str | None = None
