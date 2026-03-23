<<<<<<< HEAD
# Bot Hidratación Dockerfile - Production Ready (2026)
=======
# Multi-stage Dockerfile for bot-hidratacion
# Optimized for production with multi-stage build
>>>>>>> 877eb0b (Add Docker production configs, multi-stage Dockerfile, and Grype security scanner)

# Stage 1: Builder
FROM python:3.14-slim as builder

WORKDIR /build

# Install build dependencies
<<<<<<< HEAD
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt
=======
RUN apt-get update && apt-get install -y --no-install-recommends \
   gcc \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip wheel && \
    pip install --no-cache-dir -r requirements.txt
>>>>>>> 877eb0b (Add Docker production configs, multi-stage Dockerfile, and Grype security scanner)

# Stage 2: Production
FROM python:3.14-slim as production

<<<<<<< HEAD
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
=======
# Create non-root user for security
RUN groupadd -r botuser && useradd -r -g botuser botuser

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application files
COPY --chown=botuser:botuser . .

# Create logs directory
RUN mkdir -p /app/logs && chown -R botuser:botuser /app/logs
>>>>>>> 877eb0b (Add Docker production configs, multi-stage Dockerfile, and Grype security scanner)

# Switch to non-root user
USER botuser

<<<<<<< HEAD
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
=======
# Expose port if needed
EXPOSE 8080

# Health check
HEALTHCHECK --interval=60s --timeout=10s --start-period=30s --retries=3 \
    CMD python -c "import sys; sys.exit(0)" || exit 1

# Run the bot
>>>>>>> 877eb0b (Add Docker production configs, multi-stage Dockerfile, and Grype security scanner)
CMD ["python", "main.py"]