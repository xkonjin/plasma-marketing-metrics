'''TikTok analytics via Apify actor.

NOTE: Confirm actor name/inputs per Apify docs; returns empty list for bootstrap.
'''
from typing import List, Dict
from ingestion.config import get_settings

def fetch_videos(handle: str, since_days: int = 7) -> List[Dict]:
    _ = get_settings().apify_token
    return []