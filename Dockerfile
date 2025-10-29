# syntax=docker/dockerfile:1
FROM gcr.io/google.com/cloudsdktool/google-cloud-cli:544.0.0-emulators

RUN gcloud components install cbt --quiet

COPY --from=ghcr.io/astral-sh/uv:0.9.5 /uv /uvx /bin/

WORKDIR /app

COPY .python-version pyproject.toml uv.lock ./

ENV UV_LINK_MODE=copy
RUN --mount=type=cache,id=uv,target=/root/.cache/uv \
  uv sync

COPY entrypoint.sh ./
RUN mkdir -p /docker-entrypoint-init.d/ready.d

HEALTHCHECK --interval=10s --timeout=5s --start-period=10s --retries=5 \
  CMD [ -f /tmp/init-completed ] || exit 1

ENTRYPOINT [ "/app/entrypoint.sh" ]
