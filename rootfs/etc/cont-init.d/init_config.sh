#!/usr/bin/with-contenv bashio
# ==============================================================================
# Moving configuration.yaml this is needed for when we change the configuration
# so it overwrites the old one that are present in the volume.
# ==============================================================================

bashio::log.info "Moving configuration.yaml"
mv /etc/config/configuration.yaml /config/configuration.yaml
bashio::log.info "Moving auth file"
mkdir -p /config/.storage
mv /etc/config/.storage/* /config/.storage/
bashio::log.info "Creating default users"
uv run --with bcrypt /etc/config/scripts/create_default_users.py
rm -rf /etc/config/scripts/create_default_users.py
bashio::log.info "Initialization of configuration completed"
bashio::log.info "Available on http://localhost:8123"
