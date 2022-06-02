#!/usr/bin/with-contenv bashio
# ==============================================================================
# Moving configuration.yaml this is needed for when we change the configuration
# so it overwrites the old one that are present in the volume.
# ==============================================================================

bashio::log.info "Moving configuration.yaml"
mv /etc/config/configuration.yaml /config/configuration.yaml
