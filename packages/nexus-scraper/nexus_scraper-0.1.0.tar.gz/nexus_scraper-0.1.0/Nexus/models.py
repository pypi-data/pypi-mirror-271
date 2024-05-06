from typing import Optional

from pydantic import BaseModel, field_validator
from pydantic_settings import BaseSettings

from Nexus.exceptions import NexusInvalidInfohash, NexusSettingsException


class NexusSettings(BaseSettings):
    """
    Configuration settings for Nexus, supporting environment variables and direct initializations.

    Attributes:
    - `jackett_url`: str - URL for the Jackett service.
    - `jackett_apikey`: str - API key for the Jackett service.
    - `prowlarr_url`: str - URL for the Prowlarr service.
    - `prowlarr_apikey`: str - API key for the Prowlarr service.
    - `orionoid_client`: str - Client ID for Orionoid service.
    - `orionoid_apikey`: str - API key for Orionoid service.
    """    
    jackett_url: Optional[str] = "http://localhost:9117"
    jackett_apikey: Optional[str] = None
    prowlarr_url: Optional[str] = "http://localhost:9696"
    prowlarr_apikey: Optional[str] = None
    orionoid_client: Optional[str] = None
    orionoid_apikey: Optional[str] = None

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }

    @field_validator("prowlarr_apikey", "jackett_apikey", "orionoid_apikey", mode="before")
    def check_api_key(cls, v):
        if v and len(v) != 32:
            raise NexusSettingsException(f"API key must be 32 characters long, received {len(v)} characters.")
        return v

    @field_validator("jackett_url", "prowlarr_url", mode="before")
    def check_url(cls, v):
        if v and not v.startswith("http"):
            raise NexusSettingsException("URL must start with http or https.")
        return v


class Guids(BaseModel):
    """
    Guids class for storing scrape results.

    Attributes:
    - `imdb_id`: Optional[str] - IMDb identifier
    - `tmdb_id`: Optional[str] - TMDb identifier
    - `tvdb_id`: Optional[str] - TVDb identifier
    """
    imdb_id: Optional[str]
    tmdb_id: Optional[int]
    tvdb_id: Optional[int]

    @field_validator("imdb_id", mode="before")
    def validate_imdb(cls, v):
        """Validate and format the IMDb ID."""
        if v == 0 or v is None:
            return None
        elif isinstance(v, str) and v.startswith("tt"):
            return v
        elif isinstance(v, int):
            return f"tt{v}"
        elif v is not None and v != 0:
            return f"tt{v}"
        return v

    def __eq__(self, other):
        return self.imdb_id == other.imdb_id or self.tmdb_id == other.tmdb_id or self.tvdb_id == other.tvdb_id


class ScrapeResult(BaseModel):
    """
    ScrapeResult class for storing scrape results.
    """
    raw_title: str
    infohash: str
    source: str
    size: Optional[int] = None
    media_type: Optional[str] = None
    guids: Optional[Guids] = None
    seeders: Optional[int] = None
    leechers: Optional[int] = None

    @property
    def magnet(self):
        if not self.infohash:
            return None
        return f"magnet:?xt=urn:btih:{self.infohash}"

    @field_validator("infohash", mode="before")
    def validate_infohash(cls, v):
        if not v or not isinstance(v, str) or len(v) != 40:
            raise NexusInvalidInfohash("Valid Infohash is required.")
        return v

    @field_validator("source")
    def validate_source(cls, v):
        sources = ["annatar", "jackett", "orionoid", "prowlarr", "torbox", "torrentio"]
        if v not in sources:
            return "torrentio"
        return v

    @field_validator("media_type")
    def validate_media_type(cls, v):
        v = v.split("/")[0].lower()
        match v:
            case "tv" | "show" | "series" | "episode" | "ep" | "season":
                return "show"
            case _:
                return "movie"

    def __eq__(self, other):
        return self.infohash == other.infohash

    def __hash__(self):
        return hash(self.infohash)

    def __str__(self):
        return f"{self.raw_title} ({self.source})"
