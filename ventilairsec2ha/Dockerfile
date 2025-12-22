# https://developers.home-assistant.io/docs/add-ons/communication/add-on-docker
ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base:3.19
FROM ${BUILD_FROM}

# Install requirements
RUN apk add --no-cache \
    python3 \
    py3-pip \
    py3-setuptools \
    py3-wheel \
    py3-requests \
    py3-paho-mqtt \
    py3-aiohttp \
    py3-aiofiles \
    py3-cryptography \
    py3-pyserial \
    py3-numpy \
    py3-yaml \
    curl \
    ca-certificates

# Copy requirements
COPY rootfs/requirements.txt /tmp/
RUN pip3 install --no-cache-dir --break-system-packages -r /tmp/requirements.txt

# Copy root filesystem
COPY rootfs /

# Create non-root user for security with GPIO access
RUN addgroup -g 1000 addon && \
    adduser -D -u 1000 -G addon addon && \
    addgroup addon dialout && \
    addgroup addon gpio && \
    mkdir -p /app /data && \
    chown -R addon:addon /app /data

USER addon
WORKDIR /app

# Labels
LABEL org.opencontainers.image.title="Ventilairsec2HA"
LABEL org.opencontainers.image.description="Addon Home Assistant pour VMI Purevent Ventilairsec via EnOcean"
LABEL org.opencontainers.image.version="0.1.0"

CMD ["python3", "-u", "/app/run.py"]
