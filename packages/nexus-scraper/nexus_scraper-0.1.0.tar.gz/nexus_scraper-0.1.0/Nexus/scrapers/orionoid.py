from types import SimpleNamespace

import requests

from Nexus.exceptions import OrionoidException
from Nexus.models import Guids, NexusSettings, ScrapeResult


class Orionoid:
    """Orionoid class for Orionoid API operations."""

    def __init__(self, settings: NexusSettings):
        self.base_url = "https://api.orionoid.com"
        self.client_id = settings.orionoid_client
        self.api_key = settings.orionoid_apikey
        self.is_premium = False
        self.max_calls = 100
        self.period = 86400  # 24 hours for non-premium users
        self.is_initialized = False
        self.session = requests.Session()
        self.check_api_key_validity()

    def check_api_key_validity(self):
        """Validate the API key and initialize parameters based on the account type."""
        url = f"{self.base_url}?keyapp={self.client_id}&keyuser={self.api_key}&mode=user&action=retrieve"
        response = self.session.get(url)
        if response.status_code != 200:
            raise OrionoidException(f"API key validation failed with status code {response.status_code}")

        data = response.json()
        if data.get('result', {}).get('status') == 'success' and data.get('data', {}).get('status') == 'active':
            self.is_premium = data['data']['subscription']['package']['premium']
            self.max_calls = 1000 if self.is_premium else 100
            self.period = 3600 if self.is_premium else 86400
            self.is_initialized = True
        else:
            raise OrionoidException("Failed to initialize Orionoid due to invalid API key or account status.")

    def scrape(self, imdb_id: str, media_type: str = "movie", season=None, episode=None, limit: int = 50) -> list[ScrapeResult]:
        """Scrape Orionoid for a given media type and ID."""
        if not self.is_initialized:
            raise OrionoidException("Orionoid API not initialized.")

        if media_type not in ["movie", "show"]:
            raise OrionoidException("Invalid media type. Must be 'movie' or 'show'.")

        url = self.construct_url(media_type, imdb_id, season, episode, limit)
        response = self.session.get(url, timeout=10)
        if response.status_code != 200:
            raise OrionoidException(f"API request failed with status code {response.status_code}")

        if 'application/json' not in response.headers.get('Content-Type', ''):
            raise OrionoidException("Expected JSON response but received a different format.")

        data = response.json()["data"]["streams"]
        streams = [SimpleNamespace(**stream) for stream in data]
        return self.parse_response(streams, imdb_id, media_type)

    def construct_url(self, media_type, imdb_id, season=None, episode=None, limit = 50) -> str:
        """Construct the URL for the Orionoid API based on media type and identifiers."""
        params = {
            "keyapp": self.client_id,
            "keyuser": self.api_key,
            "mode": "stream",
            "action": "retrieve",
            "type": media_type,
            "idimdb": imdb_id,
            "streamtype": "torrent",
            "filename": "true",
            "limitcount": limit,
            "sortorder": "descending",
            "sortvalue": "best" if self.is_premium else "popularity",
        }
        if media_type == "show":
            params.update({"numberseason": season, "numberepisode": episode})
        return f"{self.base_url}?{'&'.join([f'{key}={value}' for key, value in params.items()])}"

    def parse_response(self, streams, imdb_id, media_type) -> list[ScrapeResult]:
        """Parse the response from Orionoid and create ScrapeResult objects."""
        if not streams:
            return []
        return [
            ScrapeResult(
                raw_title=stream.file["name"],
                infohash=stream.file["hash"],
                guids=Guids(
                    imdb_id=imdb_id,
                    tmdb_id=None,
                    tvdb_id=None
                ),
                media_type=media_type,
                source="orionoid"
            ) for stream in streams
        ]
