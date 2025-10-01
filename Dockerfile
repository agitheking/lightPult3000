# Multi-service container: OLA (olad) + FastAPI backend + static frontend server
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VENV_PATH=/opt/venv

# System deps + OLA + supervisor
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-venv python3-pip \
    ola ola-python \
    ca-certificates curl tini supervisor \
 && rm -rf /var/lib/apt/lists/*
# Create virtual env
RUN python3 -m venv ${VENV_PATH} && ${VENV_PATH}/bin/pip install --upgrade pip

# App
WORKDIR /app
COPY backend/requirements.txt /app/backend/requirements.txt
RUN mkdir -p /app/backend /app/frontend

RUN ${VENV_PATH}/bin/pip install -r /app/backend/requirements.txt
RUN adduser --disabled-password --gecos "" ola

# Supervisor config
COPY docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose ports:
#  - 8000 API (FastAPI)
#  - 5500 Frontend (static server)
#  - 9090 OLA Web UI
EXPOSE 8000 5500 9090

# Default is root for USB/tty access. If you prefer non-root, configure devices & udev rules accordingly.
ENTRYPOINT ["/usr/bin/tini","--"]
CMD ["supervisord","-c","/etc/supervisor/conf.d/supervisord.conf"]
