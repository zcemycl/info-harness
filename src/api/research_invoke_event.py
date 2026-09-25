"""API Gateway v2 event so Lambda Web Adapter can run research."""

from __future__ import annotations

import json
from typing import Any


def research_invoke_event(
    chat_id: str,
    run_id: str,
    brief: str,
    access_token: str,
) -> dict[str, Any]:
    """Build a payload LWA forwards to ``POST /internal/research``."""
    body = json.dumps({"chat_id": chat_id, "run_id": run_id, "brief": brief})
    return {
        "version": "2.0",
        "routeKey": "POST /internal/research",
        "rawPath": "/internal/research",
        "rawQueryString": "",
        "headers": {
            "authorization": f"Bearer {access_token}",
            "content-type": "application/json",
            "host": "localhost",
        },
        "requestContext": {
            "http": {
                "method": "POST",
                "path": "/internal/research",
                "protocol": "HTTP/1.1",
                "sourceIp": "127.0.0.1",
                "userAgent": "info-harness",
            },
            "requestId": run_id,
            "routeKey": "POST /internal/research",
            "stage": "$default",
            "timeEpoch": 0,
        },
        "body": body,
        "isBase64Encoded": False,
    }
