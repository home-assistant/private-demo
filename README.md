# Private demo

This builds an image that has the [demo](https://www.home-assistant.io/integrations/demo/) integrations enabled.
This is used for app verification and deployed with https://github.com/home-assistant/deployments

## Prerequisites

- [mise](https://mise.jdx.dev/) - Task runner and tool manager
- Docker

## Quick Start

```bash
# Build and run
mise run docker:up

# Stop
mise run docker:down
```

The instance will be available at http://localhost:8123

## Default Users

Users are created at container startup via the `DEFAULT_USERS` environment variable:

```bash
DEFAULT_USERS='[{"username":"admin","password":"secret","name":"Admin","owner":true,"admin":true}]' mise run docker:up
```

### JSON Structure

```json
[
  {"username": "admin", "password": "secret", "name": "Admin User", "owner": true, "admin": true},
  {"username": "user1", "password": "pass123", "name": "Regular User", "admin": false}
]
```

| Field | Required | Default | Description |
|-------|----------|---------|-------------|
| `username` | Yes | - | Login username |
| `password` | Yes | - | Login password |
| `name` | Yes | - | Display name |
| `owner` | No | `true` | Is owner of the instance |
| `admin` | No | `true` | Is administrator |

## Mise Tasks

### Docker

| Task | Description | Usage |
|------|-------------|-------|
| `docker:build` | Build the Docker image | `mise run docker:build` |
| `docker:build:version` | Build with specific HA version | `mise run docker:build:version 2024.1.0` |
| `docker:up` | Build and run the container | `mise run docker:up` |
| `docker:down` | Stop and remove the container | `mise run docker:down` |
| `docker:logs` | Follow container logs | `mise run docker:logs` |
| `docker:test` | Test the build | `mise run docker:test` |
| `docker:clean` | Remove built images | `mise run docker:clean` |

## Updates

- To change the configuration, adjust [`rootfs/etc/config/configuration.yaml`](./rootfs/etc/config/configuration.yaml)
- To change the Home Assistant version, use `--build-arg TARGET_VERSION=<version>` or set `TARGET_VERSION` env var with mise

After a change is merged, create a release to publish a new image. After the image is published, the [deployment can be updated](https://github.com/home-assistant/deployments/blob/main/private_demo/main.tf).

## Project Structure

```
.
├── Dockerfile
├── mise.toml                 # Task definitions
└── rootfs/
    └── etc/
        ├── config/
        │   ├── configuration.yaml
        │   ├── dashboards/
        │   │   └── build_info.yaml
        │   ├── scripts/
        │   │   └── create_default_users.py
        │   └── .storage/
        │       ├── auth
        │       ├── auth_provider.homeassistant
        │       └── onboarding
        └── cont-init.d/
            └── init_config.sh
```
