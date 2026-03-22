FROM python:3.11-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY requirements.txt .

RUN uv pip install --system --no-cache -r requirements.txt

EXPOSE 5000