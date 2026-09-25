"""Local directory or S3 text objects for chat state."""

from __future__ import annotations

import os
from pathlib import Path

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv


class ObjectStore:
    """Read and write UTF-8 objects. S3 when ``CHAT_S3_BUCKET`` is set."""

    def __init__(self) -> None:
        load_dotenv()
        self.bucket = os.getenv("CHAT_S3_BUCKET", "").strip()
        self.prefix = os.getenv("CHAT_S3_PREFIX", "").strip("/")
        self.root = _local_root()
        self._client = boto3.client("s3") if self.bucket else None

    def put_text(self, key: str, text: str) -> None:
        """Write ``key``. Creates parent directories for the local backend."""
        safe = _safe_key(key)
        if self._client is not None:
            self._client.put_object(
                Bucket=self.bucket,
                Key=self._full(safe),
                Body=text.encode("utf-8"),
                ContentType="application/json",
            )
            return
        path = self.root / safe
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def get_text(self, key: str) -> str | None:
        """Return object text, or ``None`` when the key is missing."""
        safe = _safe_key(key)
        if self._client is not None:
            return self._get_s3(safe)
        path = self.root / safe
        if not path.is_file():
            return None
        return path.read_text(encoding="utf-8")

    def delete_text(self, key: str) -> None:
        """Remove ``key``. Missing objects are ignored."""
        safe = _safe_key(key)
        if self._client is not None:
            self._client.delete_object(Bucket=self.bucket, Key=self._full(safe))
            return
        path = self.root / safe
        if path.is_file():
            path.unlink()

    def list_prefix(self, prefix: str) -> list[str]:
        """List logical keys under ``prefix``."""
        safe = _safe_key(prefix)
        if self._client is not None:
            return self._list_s3(safe)
        base = self.root / safe
        if not base.exists():
            return []
        keys: list[str] = []
        for path in base.rglob("*"):
            if path.is_file():
                keys.append(path.relative_to(self.root).as_posix())
        return sorted(keys)

    def _full(self, key: str) -> str:
        if self.prefix:
            return f"{self.prefix}/{key}"
        return key

    def _get_s3(self, key: str) -> str | None:
        assert self._client is not None
        try:
            response = self._client.get_object(
                Bucket=self.bucket,
                Key=self._full(key),
            )
        except ClientError as exc:
            code = str(exc.response.get("Error", {}).get("Code", ""))
            if code in {"NoSuchKey", "404", "NotFound"}:
                return None
            raise
        raw = response["Body"].read()
        return str(raw, encoding="utf-8")

    def _list_s3(self, prefix: str) -> list[str]:
        assert self._client is not None
        full = self._full(prefix)
        paginator = self._client.get_paginator("list_objects_v2")
        keys: list[str] = []
        for page in paginator.paginate(Bucket=self.bucket, Prefix=full):
            for item in page.get("Contents", []):
                raw = str(item["Key"])
                logical = raw[len(self.prefix) + 1 :] if self.prefix else raw
                keys.append(logical)
        return sorted(keys)


def open_object_store() -> ObjectStore:
    """Open a store from the current environment."""
    return ObjectStore()


def _local_root() -> Path:
    configured = os.getenv("CHAT_DATA_DIR", "").strip()
    if configured:
        return Path(configured)
    if os.getenv("AWS_LAMBDA_FUNCTION_NAME"):
        return Path("/tmp/chats")
    return Path("data/chats")


def _safe_key(key: str) -> str:
    cleaned = key.strip().lstrip("/")
    if not cleaned or ".." in cleaned.split("/"):
        raise ValueError(f"unsafe object key: {key}")
    return cleaned
