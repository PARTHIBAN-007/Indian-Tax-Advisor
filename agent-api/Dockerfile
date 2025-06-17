FROM python:3.11-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app
COPY uv.lock pyproject.toml README.md ./
RUN uv sync --frozen --no-cache
COPY . .
ENV PYTHONPATH="${PYTHONPATH}:/app/src"
CMD ["uvicorn", "infrastructure.api:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]

