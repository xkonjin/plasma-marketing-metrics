'''Typefully-based ingestors for X and LinkedIn.

NOTE: Fill in endpoints/params per official Typefully API docs.
These functions return empty lists by default to allow safe runs.
'''
from typing import List, Dict
from ingestion.config import get_settings

def fetch_x_posts(since_days: int = 7) -> List[Dict]:
    _ = get_settings().typefully_api_key
    # TODO: Implement with Typefully API once metrics endpoints are confirmed.
    return []

def fetch_linkedin_posts(since_days: int = 7) -> List[Dict]:
    _ = get_settings().typefully_api_key
    # TODO: Implement with Typefully API once metrics endpoints are confirmed.
    return []