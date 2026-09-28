# syntax=docker/dockerfile:1
# Local FastAPI image. Compose bind-mounts ./src and ./data on top of this.
# Dependencies are installed at build time. Compose passes PRIVATE_REPO_TOKEN
# from the root .env so the private hc-datacore git dependency can be cloned.
# 3.12: hc-datacore pins lxml==4.9.4, which has no cp313 wheel.

FROM public.ecr.aws/docker/library/python:3.12-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:0.11.17 /uv /bin/uv

ARG PRIVATE_REPO_TOKEN

WORKDIR /var/task

COPY pyproject.toml uv.lock README.md ./
COPY vendor ./vendor

RUN --mount=type=ssh,required=false \
    if [ -n "${PRIVATE_REPO_TOKEN}" ]; then \
      git config --global url."https://x-token-auth:${PRIVATE_REPO_TOKEN}@github.com".insteadOf "ssh://git@github.com"; \
    fi \
    && uv export --frozen --no-dev --no-emit-project --no-hashes \
        -o /tmp/requirements.txt \
    && uv pip install --system --no-cache --python /usr/local/bin/python \
        -r /tmp/requirements.txt \
    && site="$(/usr/local/bin/python -c 'import site; print(site.getsitepackages()[0])')" \
    && rm -rf "$site/asyncio" "$site"/asyncio-*.dist-info "$site"/asyncio-*.egg-info \
    && rm -f /root/.gitconfig /tmp/requirements.txt

ENV PORT=8080 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    WATCHFILES_FORCE_POLLING=true

EXPOSE 8080

CMD ["uvicorn", "--app-dir", "src", "--host", "0.0.0.0", "--port", "8080", "--reload", "--reload-dir", "src", "--timeout-keep-alive", "120", "api.app:app"]
