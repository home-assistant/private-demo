ARG TARGET_VERSION=stable
FROM ghcr.io/home-assistant/home-assistant:$TARGET_VERSION
COPY rootfs /
