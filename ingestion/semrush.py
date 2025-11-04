'''Semrush keyword/backlink ingestion.

NOTE: Verify API endpoints/types with Semrush docs before enabling.
Returns empty lists by default for safe bootstrap.
'''
from typing import List, Dict
from ingestion.config import get_settings

def fetch_keywords(domain: str, since_days: int = 7) -> List[Dict]:
    _ = get_settings().semrush_api_key
    return []

def fetch_backlinks(domain: str, since_days: int = 7) -> List[Dict]:
    _ = get_settings().semrush_api_key
    return []