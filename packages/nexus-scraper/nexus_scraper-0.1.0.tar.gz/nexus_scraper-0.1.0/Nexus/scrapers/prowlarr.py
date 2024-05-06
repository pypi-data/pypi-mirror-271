from types import SimpleNamespace

import requests

from Nexus.exceptions import ProwlarrException
from Nexus.models import Guids, NexusSettings, ScrapeResult


class Prowlarr:
    """Prowlarr class for Prowlarr API operations."""

    def __init__(self, settings: NexusSettings):
        if not settings.prowlarr_url or not settings.prowlarr_apikey != 32:
            raise ProwlarrException("Prowlarr: URL and API key are required.")

        self.api_key = settings.prowlarr_apikey
        self.base_url = settings.prowlarr_url
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {self.api_key}"})

    def _request(self, endpoint, method="GET", params=None, data=None, timeout=60):
        if endpoint.startswith("/"):
            url = f"{self.base_url}{endpoint}"
        else:
            url = f"{self.base_url}/api/v1/{endpoint}"
        try:
            response = self.session.request(method, url, params=params, json=data, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise ProwlarrException(f"Prowlarr: API request error: {str(e)}")

    def scrape(self, query, media_type = None, limit = 50, timeout = 60) -> list[ScrapeResult]:
        """Scrape Prowlarr for a given query."""
        if not isinstance(limit, int):
            raise ProwlarrException("Prowlarr: Limit must be an integer.")

        if query.startswith("tt"):
            return []

        data = self._request("search", params={"categories": [2000, 5000], "query": query, "limit": limit}, timeout=timeout)
        if not data:
            return []

        container = [SimpleNamespace(**result) for result in data]

        results = []
        for result in container:
            try:
                guids = Guids(
                    imdb_id=result.imdbId if result.imdbId != 0 else None,
                    tmdb_id=result.tmdbId if result.tmdbId != 0 else None,
                    tvdb_id=result.tvdbId if result.tvdbId != 0 else None,
                )
                scrape_result = ScrapeResult(
                    raw_title=result.title,
                    infohash=result.infoHash,
                    guids=guids,
                    media_type=result.categories[0].get("name", None),
                    source="prowlarr",
                    size=result.size,
                    seeders=result.seeders,
                    leechers=result.leechers,
                )
                results.append(scrape_result)
            except AttributeError:
                continue

        if not results:
            return []
        return results

    def ping(self):
        """Ping the Prowlarr API."""
        return self._request("/ping")
