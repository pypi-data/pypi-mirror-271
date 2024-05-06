import requests

from Nexus.exceptions import TorrentioException
from Nexus.models import Guids, ScrapeResult


class Torrentio:
    """Torrentio class for Torrent API operations."""

    def __init__(self, url: str = "https://torrentio.strem.fun", filters: str = "qualityfilter=other,scr,cam"):
        self.base_url = url
        self.filters = filters
        self.session = requests.Session()

    def _request(self, endpoint: str):
        url = f"{self.base_url}/{self.filters}/{endpoint}.json"
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise TorrentioException(f"Torrentio: API request error: {e}")

    def scrape(self, imdbid: str, media_type: str = "", season: int = 9999, episode: int = 9999, limit: int = 50) -> list[ScrapeResult]:
        """Scrape Torrentio for a given query."""
        if not imdbid:
            raise TorrentioException("Torrentio: IMDB ID is required.")

        if not imdbid.startswith("tt"):
            raise TorrentioException("Torrentio: Invalid IMDB ID.")

        if not media_type:
            raise TorrentioException("Torrentio: Media type is required.")

        # lets de-normalize it here
        if media_type.lower() == "show":
            media_type = "series"

        if media_type not in ["movie", "series"]:
            raise TorrentioException("Invalid media type. Must be 'movie' or 'show'.")

        endpoint = f"stream/movie/{imdbid}"
        if media_type.lower() == "series" and season != 9999 and episode != 9999:
            endpoint = f"stream/series/{imdbid}:{season}:{episode}"

        res = self._request(endpoint)
        if not res or "streams" not in res:
            return []

        return [
            ScrapeResult(
                raw_title=result["title"].split("\n👤")[0].split("\n")[0],
                infohash=result["infoHash"],
                guids=Guids(
                    imdb_id=imdbid,
                    tmdb_id=None,
                    tvdb_id=None
                ),
                media_type=media_type.lower(),
                source="torrentio",
                size=result.get("size", None),
                seeders=result.get("seeders", None),
                leechers=result.get("leechers", None)
            ) for result in res["streams"]
        ]

    def ping(self):
        """Ping the Torrentio API."""
        return self._request("ping")
