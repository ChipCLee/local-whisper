FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/app/.venv/bin:$PATH" \
    HF_HOME="/models/huggingface" \
    WHISPER_MODEL="large-v3-turbo" \
    WHISPER_DEVICE="cpu" \
    WHISPER_COMPUTE_TYPE="int8" \
    WHISPER_PORT=9000

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:0.8.23 /uv /uvx /bin/

COPY pyproject.toml uv.lock README.md ./
RUN uv sync --locked --no-dev --no-install-project

COPY server.py start.sh ./

RUN useradd --create-home --uid 10001 appuser \
    && mkdir -p /models/huggingface \
    && chown -R appuser:appuser /app /models

USER appuser

EXPOSE 9000

CMD ["python", "server.py"]
