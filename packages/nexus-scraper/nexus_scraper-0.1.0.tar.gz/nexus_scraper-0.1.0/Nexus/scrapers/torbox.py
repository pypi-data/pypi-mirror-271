from typing import List

from Nexus.models import ScrapeResult


class TorBox:
    def __init__(self):
        self.url = "https://torbox.net"

    def _request(self, endpoint, method="GET", params=None, data=None, timeout=30):
        return []

    def scrape(self, query, limit = 50, media_type = "movie", timeout = 30) -> List[ScrapeResult]:
        return []
