FROM gcr.io/google.com/cloudsdktool/google-cloud-cli:517.0.0-emulators

COPY --from=ghcr.io/astral-sh/uv:0.6.14 /uv /uvx /bin/

WORKDIR /app

COPY .python-version pyproject.toml uv.lock ./

RUN uv sync

RUN mkdir -p /docker-entrypoint-init.d/ready.d

COPY entrypoint.sh ./

ENTRYPOINT [ "/app/entrypoint.sh" ]
