FROM python:3.12.7-slim@sha256:60d9996b6a8a3689d36db740b49f4327be3be09a21122bd02fb8895abb38b50d

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src
ENV EOA_HOST=0.0.0.0
ENV EOA_PORT=8085
ENV EOA_STATE_DIR=/var/lib/enterprise-orchestrator

WORKDIR /app

COPY pyproject.toml README.md STATUS.md ./
COPY prompts ./prompts
COPY src ./src
COPY ui ./ui

RUN useradd --system --create-home --home-dir /var/lib/enterprise-orchestrator eoa \
    && chown -R eoa:eoa /var/lib/enterprise-orchestrator /app

USER eoa

EXPOSE 8085

CMD ["python", "-m", "enterprise_orchestrator.app"]
