# Multi-stage Dockerfile with Python Slim
# Optimized for size and performance (~150-200MB)

# Stage 1: Builder
FROM python:3.12-slim AS builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies to a specific location
RUN pip install --prefix=/install --no-cache-dir --no-warn-script-location -r requirements.txt

# Stage 2: Runtime
FROM python:3.12-slim

WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH=/usr/local/bin:$PATH

# Copy Python dependencies from builder
COPY --from=builder /install /usr/local

# Copy application files
COPY mcp_pipe.py .
COPY mcp_config.json .
COPY *.py ./

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)" || exit 1

CMD ["python", "mcp_pipe.py"]
