FROM gcr.io/google.com/cloudsdktool/google-cloud-cli:517.0.0-emulators

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      python3.11=3.11.2-6+deb12u5 \
      python3.11-venv=3.11.2-6+deb12u5 && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /requirements.txt

RUN python3 -m venv /venv && \
  . /venv/bin/activate && \
  pip install --no-cache-dir -r /requirements.txt

RUN mkdir -p /docker-entrypoint-init.d/ready.d

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]
