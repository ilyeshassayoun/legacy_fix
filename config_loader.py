# config_loader.py
# Reads settings.cfg. Hand-rolled, because ConfigParser felt "too complicated" in 2013.

SETTINGS_FILE = "settings.cfg"

KNOWN_KEYS = [
    "service_interval_km",
    "warn_at_percent",
    "report_title",
    "history_file",
    "log_file",
    "mileage_unit",
]


def load_settings(path: str | None = None) -> dict[str, str]:
    """Parse settings.cfg and return a dict of known keys to their string values."""
    if path is None:
        path = SETTINGS_FILE
    settings: dict[str, str] = {}
    try:
        f = open(path)
    except FileNotFoundError:
        return settings
    with f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip()
            if key in KNOWN_KEYS:
                settings[key] = value
    return settings


def get_int(settings: dict[str, str], key: str, fallback: int) -> int:
    """Return the integer value for key, or fallback if missing or not a valid int."""
    try:
        return int(settings[key])
    except (KeyError, ValueError):
        return fallback


def get_setting(settings: dict[str, str], key: str, fallback: str = "") -> str:
    """Return the string value for key, or fallback if not present."""
    return settings.get(key, fallback)
