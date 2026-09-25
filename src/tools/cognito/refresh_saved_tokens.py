"""Refresh saved Cognito JWTs with the stored refresh token."""

from __future__ import annotations

import boto3

from model.cognito_config import CognitoConfig
from model.cognito_tokens import CognitoTokens
from tools.load_cognito_tokens import load_cognito_tokens
from tools.save_cognito_tokens import save_cognito_tokens


def refresh_saved_tokens() -> CognitoTokens:
    """Replace expired id/access tokens and keep the existing refresh token."""
    current = load_cognito_tokens()
    if not current.refresh_token:
        raise RuntimeError(
            "Cognito refresh token missing. Run: "
            "uv run python src/main.py cognito-login -u <username>"
        )
    config = CognitoConfig.from_env()
    client = boto3.client("cognito-idp", region_name=config.region)
    response = client.initiate_auth(
        ClientId=config.user_pool_client_id,
        AuthFlow="REFRESH_TOKEN_AUTH",
        AuthParameters={"REFRESH_TOKEN": current.refresh_token},
    )
    result = response.get("AuthenticationResult") or {}
    if "AccessToken" not in result or "IdToken" not in result:
        raise RuntimeError("Cognito refresh did not return new tokens.")
    updated = current.model_copy(
        update={
            "id_token": result["IdToken"],
            "access_token": result["AccessToken"],
            "expires_in": result.get("ExpiresIn"),
            "token_type": result.get("TokenType"),
        }
    )
    save_cognito_tokens(updated)
    return updated
