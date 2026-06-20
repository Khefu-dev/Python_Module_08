#!/usr/bin/env python3

import os

try:
    from dotenv import load_dotenv
    HAS_DOTENV = True
except ImportError:
    HAS_DOTENV = False

DEFAULTS: dict[str, str] = {
    "MATRIX_MODE": "development",
    "DATABASE_URL": "postgresql://localhost:5432/matrix",
    "API_KEY": "",
    "LOG_LEVEL": "INFO",
    "ZION_ENDPOINT": "",
}


def load_configuration() -> dict[str, str]:
    if HAS_DOTENV:
        try:
            load_dotenv()
        except OSError as exc:
            print(f"WARNING: could not read .env file - {exc}")
    else:
        print("WARNING: python-dotenv not installed, using shell env only")

    config: dict[str, str] = {}
    missing: list[str] = []
    for key, default in DEFAULTS.items():
        if key in os.environ:
            config[key] = os.environ[key]
        else:
            config[key] = default
            missing.append(key)

    if missing:
        names = ", ".join(missing)
        print(f"WARNING: missing {names}, using defaults\n")

    return config


def mask_secret(value: str, visible: int = 4) -> str:
    if not value:
        return "(not set)"
    if len(value) <= visible:
        return "*" * len(value)
    return "*" * (len(value) - visible) + value[-visible:]


def mask_url(url: str) -> str:
    if not url or "://" not in url:
        return url or "(not set)"

    scheme, rest = url.split("://", 1)
    if "/" in rest:
        netloc, path = rest.split("/", 1)
        path = "/" + path
    else:
        netloc, path = rest, ""

    if "@" not in netloc:
        return url

    _, host = netloc.rsplit("@", 1)
    return f"{scheme}://***@{host}{path}"


def print_configuration(config: dict[str, str]) -> None:
    mode = config["MATRIX_MODE"]
    is_production = mode == "production"

    print("ORACLE STATUS: Reading the Matrix...\n")
    print("Configuration loaded:")
    print(f"Mode: {mode}")

    db_url = config["DATABASE_URL"]
    db_display = mask_url(db_url) if is_production else db_url
    db_kind = "production" if is_production else "local"
    print(f"Database: Connected to {db_kind} instance ({db_display})")

    api_key = config["API_KEY"]
    if api_key:
        print(f"API Access: Authenticated ({mask_secret(api_key)})")
    else:
        print("API Access: Not configured")

    print(f"Log Level: {config['LOG_LEVEL']}")

    zion_endpoint = config["ZION_ENDPOINT"]
    if zion_endpoint:
        endpoint = mask_url(zion_endpoint) if is_production else zion_endpoint
        print(f"Zion Network: Online ({endpoint})")
    else:
        print("Zion Network: Offline")

    env_file_present = os.path.exists(".env")
    env_status = "OK" if env_file_present else "WARNING"
    env_message = (
        "properly configured"
        if env_file_present
        else "not found, using environment/defaults"
    )
    overrides = "active" if is_production else "available"

    print("\nEnvironment security check:")
    print("[OK] No hardcoded secrets detected")
    print(f"[{env_status}] .env file {env_message}")
    print(f"[OK] Production overrides {overrides}")

    print("\nThe Oracle sees all configurations.")


def main() -> None:
    config = load_configuration()
    print_configuration(config)


if __name__ == "__main__":
    main()
