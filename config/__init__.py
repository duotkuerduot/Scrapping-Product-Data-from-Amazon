from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

DEFAULT_CONFIG: Dict[str, Any] = {
    "root_url": "https://www.amazon.in/gp/bestsellers/kitchen/3474656031",
    "output_csv": "amazon_top50.csv",
    "max_products": 50,
}


def _coerce_value(key: str, raw: str) -> Any:
    if key == "max_products":
        try:
            return int(raw)
        except ValueError:
            return DEFAULT_CONFIG["max_products"]
    return raw


def load_config(path: Path | None = None) -> Dict[str, Any]:
    config_path = path or Path(__file__).with_name("config.yaml")
    data = DEFAULT_CONFIG.copy()
    if not config_path.exists():
        return data

    for line in config_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip("\"").strip("'")
        data[key] = _coerce_value(key, value)

    return data
