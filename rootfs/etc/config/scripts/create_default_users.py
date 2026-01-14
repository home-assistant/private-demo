#!/usr/bin/env python3
"""Create default Home Assistant users from JSON environment variable.

Environment variable DEFAULT_USERS should contain JSON array:
[
  {"username": "admin", "password": "secret", "name": "Admin User", "owner": true, "admin": true},
  {"username": "user1", "password": "pass123", "name": "Regular User", "admin": false}
]

Fields:
  - username: Login username (required)
  - password: Login password (required)
  - name: Display name (required)
  - owner: Is owner (optional, default: true)
  - admin: Is admin (optional, default: true)
"""

import argparse
import base64
import json
import os
import sys
import uuid
from pathlib import Path

import bcrypt


def generate_id() -> str:
    """Generate a Home Assistant compatible ID (32 hex chars, no dashes)."""
    return uuid.uuid4().hex


def hash_password(password: str) -> str:
    """Hash a password in Home Assistant's storage format."""
    hashed = bcrypt.hashpw(password.encode()[:72], bcrypt.gensalt(rounds=12))
    return base64.b64encode(hashed).decode()


def create_users(storage_path: Path) -> None:
    """Create users from DEFAULT_USERS environment variable."""
    users_json = os.environ.get("DEFAULT_USERS")

    if not users_json:
        print("No users to create (DEFAULT_USERS not set)")
        return

    try:
        users = json.loads(users_json)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in DEFAULT_USERS: {e}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(users, list):
        print("Error: DEFAULT_USERS must be a JSON array", file=sys.stderr)
        sys.exit(1)

    auth_file = storage_path / "auth"
    provider_file = storage_path / "auth_provider.homeassistant"

    # Read existing files
    with open(auth_file) as f:
        auth_data = json.load(f)

    with open(provider_file) as f:
        provider_data = json.load(f)

    # Get existing usernames
    existing_usernames = {
        u["username"].strip().casefold() for u in provider_data["data"]["users"]
    }

    created = 0
    for user in users:
        # Validate required fields
        if not all(k in user for k in ("username", "password", "name")):
            print(f"Error: User missing required fields (username, password, name): {user}", file=sys.stderr)
            sys.exit(1)

        username = user["username"]
        password = user["password"]
        display_name = user["name"]
        is_owner = user.get("owner", True)
        is_admin = user.get("admin", True)

        normalized = username.strip().casefold()

        if normalized in existing_usernames:
            print(f"Skipping '{username}' (already exists)")
            continue

        user_id = generate_id()
        credential_id = generate_id()

        # Create user entry in auth
        group_id = "system-admin" if is_admin else "system-users"
        auth_data["data"]["users"].append({
            "id": user_id,
            "group_ids": [group_id],
            "is_owner": is_owner,
            "is_active": True,
            "name": display_name,
            "system_generated": False,
            "local_only": False,
        })

        # Create credential entry in auth
        auth_data["data"]["credentials"].append({
            "id": credential_id,
            "user_id": user_id,
            "auth_provider_type": "homeassistant",
            "auth_provider_id": None,
            "data": {"username": username},
        })

        # Create provider entry
        provider_data["data"]["users"].append({
            "username": username,
            "password": hash_password(password),
        })

        existing_usernames.add(normalized)
        created += 1
        print(f"Created user '{username}' ({display_name})")

    # Write files back
    with open(auth_file, "w") as f:
        json.dump(auth_data, f, indent=2)

    with open(provider_file, "w") as f:
        json.dump(provider_data, f, indent=2)

    print(f"Created {created} user(s)")


def main() -> None:
    parser = argparse.ArgumentParser(description="Create default Home Assistant users from DEFAULT_USERS env var")
    parser.add_argument(
        "--storage",
        "-s",
        type=Path,
        default=Path("/config/.storage"),
        help="Path to .storage directory",
    )
    args = parser.parse_args()

    create_users(args.storage)


if __name__ == "__main__":
    main()
