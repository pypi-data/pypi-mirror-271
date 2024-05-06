from typing import List

from Nexus.models import ScrapeResult


class Annatar:
    def __init__(self):
        self.url = "https://annatar.elfhosted.com"

    def _request(self, endpoint, method="GET", params=None, data=None, timeout=30):
        return []

    def scrape(self, query, limit = 50, media_type = "movie", timeout = 30) -> List[ScrapeResult]:
        return []
