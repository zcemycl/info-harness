# syntax=docker/dockerfile:1
# FastAPI on AWS Lambda via the Web Adapter (response streaming).
# The CLI stays `src/main.py` and is not the container command.
#
# Build (private hc-datacore via SSH):
#   DOCKER_BUILDKIT=1 docker build --ssh default -t info-harness .
# CI passes --build-arg PRIVATE_REPO_TOKEN instead of SSH.
#
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

COPY src ./src

COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.9.1 /lambda-adapter /opt/extensions/lambda-adapter

ENV PORT=8000
ENV AWS_LWA_PORT=8000
ENV AWS_LWA_INVOKE_MODE=response_stream
ENV AWS_LWA_READINESS_CHECK_PATH=/health
ENV AWS_LWA_READINESS_CHECK_PORT=8000

CMD exec uvicorn --app-dir src --host 0.0.0.0 --port "$PORT" --timeout-keep-alive 120 api.app:app
