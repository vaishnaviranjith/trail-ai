# ======================================================
# Trail AI (Smart Trip Planner MVP) - Multi-Stage Dockerfile
# Based on IEEE Research Framework (DOI: 10.1109/ICUIS67429.2025.11380545)
# ======================================================

# Stage 1: Build Frontend Assets
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend

COPY ["trail ai/frontend/package.json", "./"]
RUN npm install --no-audit --no-fund

COPY ["trail ai/frontend/", "./"]
RUN npm run build

# Stage 2: Production Python Backend Runtime
FROM python:3.11-slim AS production

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ["trail ai/backend/", "./backend/"]
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

WORKDIR /app/backend
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
