FROM ghcr.io/astral-sh/uv:alpine

WORKDIR /app

COPY pyproject.toml .
COPY uv.lock .

RUN apk add build-base zlib-dev
RUN uv sync --locked

COPY ./src .


CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]