ARG TARGET_VERSION=stable
FROM ghcr.io/home-assistant/home-assistant:$TARGET_VERSION

COPY rootfs /

ARG BUILD_DATE
RUN echo "${BUILD_DATE:-$(date -Iseconds)}" > /config/build_date.txt

ENV DEFAULT_USERS='[]'
