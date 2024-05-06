from typing import List

from Nexus.models import NexusSettings, ScrapeResult


class Jackett:
    def __init__(self, settings: NexusSettings):
        self.settings = settings

    def _request(self, endpoint, method="GET", params=None, data=None, timeout=30):
        return []

    def scrape(self, query, limit = 50, media_type = "movie", timeout = 30) -> List[ScrapeResult]:
        return []
