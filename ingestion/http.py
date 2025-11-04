'''Resilient HTTP client utilities using httpx + backoff.

Provides get_json and post_json with exponential backoff and timeouts.
'''
from typing import Any, Dict, Optional
import httpx
import backoff
from ingestion.config import get_settings

def _client() -> httpx.Client:
    s = get_settings()
    return httpx.Client(timeout=s.http_timeout_seconds)

def _give_up(exc: Exception) -> bool:
    # For 4xx (except 429), don't retry
    if isinstance(exc, httpx.HTTPStatusError):
        status = exc.response.status_code
        return status < 500 and status != 429
    return False

@backoff.on_exception(
    backoff.expo,
    (httpx.TransportError, httpx.HTTPStatusError),
    giveup=_give_up,
    max_tries=5,
)
def get_json(url: str, headers: Optional[Dict[str, str]] = None, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    with _client() as client:
        resp = client.get(url, headers=headers, params=params)
        resp.raise_for_status()
        return resp.json()

@backoff.on_exception(
    backoff.expo,
    (httpx.TransportError, httpx.HTTPStatusError),
    giveup=_give_up,
    max_tries=5,
)
def post_json(url: str, headers: Optional[Dict[str, str]] = None, json_body: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    with _client() as client:
        resp = client.post(url, headers=headers, json=json_body)
        resp.raise_for_status()
        return resp.json()