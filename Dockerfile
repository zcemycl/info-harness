# syntax=docker/dockerfile:1
# FastAPI on AWS Lambda. The CLI stays `src/main.py` and is not the container command.
#
# Build (private hc-datacore via SSH):
#   DOCKER_BUILDKIT=1 docker build --ssh default -t info-harness .
#
# Lambda handler: api.lambda_handler.handler
#   HTTP goes to FastAPI. Payload {"action":"research",...} runs the same
#   pipeline as `main.py agent research`.
# Local API: uv run uvicorn api.app:app --host 0.0.0.0 --port 8080
# CLI:       uv run python src/main.py agent research "..."

FROM public.ecr.aws/lambda/python:3.13

COPY --from=ghcr.io/astral-sh/uv:0.11.17 /uv /bin/uv

WORKDIR /tmp/app
COPY pyproject.toml uv.lock README.md ./
COPY vendor ./vendor

RUN --mount=type=ssh \
    uv export --frozen --no-dev --no-emit-project --no-hashes \
        -o /tmp/requirements.txt \
    && uv pip install --python /var/lang/bin/python \
        --target "${LAMBDA_TASK_ROOT}" -r /tmp/requirements.txt

COPY src/ ${LAMBDA_TASK_ROOT}/

CMD ["api.lambda_handler.handler"]
