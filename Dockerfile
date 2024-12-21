FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY requirements.txt .

# RUN uv venv .venv

# RUN uv pip install --no-cache-dir -r requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# ENV PATH="/app/.venv/bin:$PATH"

ENTRYPOINT []