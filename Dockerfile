FROM gcr.io/google.com/cloudsdktool/google-cloud-cli:517.0.0-emulators

RUN apt-get update && \
    apt-get install -y python3.11 python3.11-venv && \
    rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /venv && \
  . /venv/bin/activate && \
  pip install \
    google-cloud-bigtable \
    google-cloud-datastore \
    google-cloud-firestore \
    google-cloud-pubsub \
    google-cloud-spanner

RUN mkdir -p /docker-entrypoint-init.d/ready.d

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]
