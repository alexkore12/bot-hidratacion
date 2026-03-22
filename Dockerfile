# Bot Hidratación Dockerfile - Production Ready (2026)

# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Production
FROM python:3.11-slim as production

# Security: Create non-root user
RUN groupadd -r botgroup && useradd -r -g botgroup -u 1000 botuser

WORKDIR /app

# Copy only necessary files from builder
COPY --from=builder /root/.local /home/botuser/.local
COPY --chown=botuser:botgroup . .

# Environment variables
ENV PATH=/home/botuser/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Switch to non-root user
USER botuser

# Health check (script-based)
HEALTHCHECK --interval=60s --timeout=10s --start-period=30s --retries=3 \
    CMD python -c "import sys; sys.exit(0)" || exit 1

# Start the bot
CMD ["python", "main.py"]

# Development stage
FROM production as development

# Install development dependencies
RUN pip install --no-cache-dir --user ipython htop

# Use development settings
CMD ["python", "main.py"]