"""FastAPI application. Local: uvicorn. Lambda: Web Adapter in front of uvicorn."""

from __future__ import annotations

import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import mount_routes
from model.billing.billing_config import BillingConfig
from tools.billing.ensure_billing_tables import ensure_billing_tables


def create_app() -> FastAPI:
    """Build the HTTP app. Does not register Typer commands."""
    load_dotenv()
    BillingConfig.from_env()
    ensure_billing_tables()
    app = FastAPI(title="info-harness", version="0.1.0")
    raw = os.getenv("CORS_ALLOW_ORIGINS", "*")
    origins = [item.strip() for item in raw.split(",") if item.strip()]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins or ["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    mount_routes(app)
    return app


app = create_app()
