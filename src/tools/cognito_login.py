"""Log in to Cognito with username/password and return JWTs."""

from __future__ import annotations

import boto3
from botocore.exceptions import ClientError

from model.cognito_config import CognitoConfig
from model.cognito_tokens import CognitoTokens
from tools.save_cognito_tokens import save_cognito_tokens


def run_cognito_login(username: str, password: str) -> CognitoTokens:
    """Authenticate against Cognito USER_PASSWORD_AUTH, save, and return tokens."""
    config = CognitoConfig.from_env()
    client = boto3.client("cognito-idp", region_name=config.region)
    try:
        response = client.initiate_auth(
            ClientId=config.user_pool_client_id,
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={"USERNAME": username, "PASSWORD": password},
        )
    except ClientError as exc:
        code = exc.response.get("Error", {}).get("Code", "ClientError")
        message = exc.response.get("Error", {}).get("Message", str(exc))
        raise RuntimeError(f"Cognito login failed ({code}): {message}") from exc

    if "ChallengeName" in response:
        challenge = response["ChallengeName"]
        raise RuntimeError(
            f"Cognito login requires additional challenge: {challenge}. "
            "Complete that flow in the Cognito console or app first."
        )

    result = response.get("AuthenticationResult")
    if not result or "IdToken" not in result or "AccessToken" not in result:
        raise RuntimeError("Cognito login succeeded but no tokens were returned.")

    tokens = CognitoTokens(
        id_token=result["IdToken"],
        access_token=result["AccessToken"],
        refresh_token=result.get("RefreshToken"),
        expires_in=result.get("ExpiresIn"),
        token_type=result.get("TokenType"),
    )
    save_cognito_tokens(tokens)
    return tokens
