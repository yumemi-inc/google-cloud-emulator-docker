FROM gcr.io/google.com/cloudsdktool/google-cloud-cli:531.0.0-emulators

RUN gcloud components install cbt --quiet

COPY --from=ghcr.io/astral-sh/uv:0.6.14 /uv /uvx /bin/

WORKDIR /app

COPY .python-version pyproject.toml uv.lock ./

RUN uv sync && \
    mkdir -p /docker-entrypoint-init.d/ready.d

COPY entrypoint.sh ./

HEALTHCHECK --interval=10s --timeout=5s --start-period=10s --retries=5 \
  CMD [ -f /tmp/init-completed ] || exit 1

ENTRYPOINT [ "/app/entrypoint.sh" ]
