'''Centralized configuration using environment variables.

This module provides a typed configuration object for all ingestion jobs.
It can be imported by scripts under scripts/ to ensure consistent env usage.
'''
from pydantic import BaseSettings
from typing import Optional
import base64
import json

class Settings(BaseSettings):
    database_url: str
    typefully_api_key: Optional[str] = None
    semrush_api_key: Optional[str] = None
    apify_token: Optional[str] = None
    ga4_json_key_b64: Optional[str] = None
    ga4_property_id: Optional[str] = None
    http_timeout_seconds: int = 30
    http_max_retries: int = 3
    backoff_base_seconds: float = 1.0

    class Config:
        env_prefix = ""
        case_sensitive = False

def get_settings() -> Settings:
    return Settings()

def decode_ga4_credentials(settings: Settings) -> Optional[dict]:
    if not settings.ga4_json_key_b64:
        return None
    data = base64.b64decode(settings.ga4_json_key_b64.encode("utf-8"))
    return json.loads(data.decode("utf-8"))