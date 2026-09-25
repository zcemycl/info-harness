"""Register FastAPI routers."""

from __future__ import annotations

from fastapi import APIRouter, Depends, FastAPI

from api.require_access_token import require_access_token
from api.routes.create_chat import router as create_chat_router
from api.routes.delete_chat import router as delete_chat_router
from api.routes.get_chat import router as get_chat_router
from api.routes.get_events import router as get_events_router
from api.routes.get_run import router as get_run_router
from api.routes.health import router as health_router
from api.routes.list_chats import router as list_chats_router
from api.routes.post_message import router as post_message_router
from api.routes.stream_events import router as stream_events_router


def mount_routes(app: FastAPI) -> None:
    """Attach chat and run routes. CLI is not mounted here."""
    app.include_router(health_router)
    protected = APIRouter(dependencies=[Depends(require_access_token)])
    routers: tuple[APIRouter, ...] = (
        create_chat_router,
        delete_chat_router,
        list_chats_router,
        get_chat_router,
        post_message_router,
        get_run_router,
        get_events_router,
        stream_events_router,
    )
    for router in routers:
        protected.include_router(router)
    app.include_router(protected)
