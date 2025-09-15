#!/usr/bin/env python3
"""
Centralized configuration for Dashscope API.

- Reads `DASHSCOPE_API_KEY` and `DASHSCOPE_API_BASE` from environment.
- Optionally loads a local `.env` file (simple parser) if present.
- Provides helpers for HTTP headers and validation.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict


def _load_dotenv_if_present() -> None:
    """Load simple KEY=VALUE pairs from a local `.env` if it exists.

    Notes:
    - Only sets keys that are not already set in the environment.
    - Ignores blank lines and lines starting with `#`.
    - This avoids adding a runtime dependency on `python-dotenv`.
    """

    env_path = Path(".env")
    if not env_path.exists():
        return

    try:
        for raw in env_path.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            # Do not override existing env values
            if key and key not in os.environ:
                os.environ[key] = value
    except Exception:
        # Silent fallback; config validation will surface issues later.
        pass


@dataclass(frozen=True)
class Settings:
    api_key: str
    api_base: str

    @property
    def headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }


def load_settings() -> Settings:
    """Load and validate settings from env (or `.env`)."""
    _load_dotenv_if_present()

    api_key = os.getenv("DASHSCOPE_API_KEY")
    api_base = os.getenv(
        "DASHSCOPE_API_BASE",
        "https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    if not api_key or not api_key.strip():
        raise RuntimeError(
            "DASHSCOPE_API_KEY is not set. Configure it via environment or .env"
        )

    if not api_base or not api_base.strip():
        raise RuntimeError("DASHSCOPE_API_BASE is not set or empty.")

    return Settings(api_key=api_key.strip(), api_base=api_base.strip())

