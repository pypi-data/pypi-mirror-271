class NexusException(Exception):
    """Custom exception for scraping errors."""

class NexusSettingsException(NexusException):
    """Custom exception for NexusSettings errors."""

class NexusInvalidInfohash(NexusException):
    """Custom exception for infohash errors."""

class AnnatarException(NexusException):
    """Custom exception for Annatar API errors."""

class JackettException(NexusException):
    """Custom exception for Jackett API errors."""

class OrionoidException(NexusException):
    """Custom exception for Orionoid API errors."""

class ProwlarrException(NexusException):
    """Custom exception for Prowlarr API errors."""

class TorBoxException(NexusException):
    """Custom exception for TorBox API errors."""

class TorrentioException(NexusException):
    """Custom exception for Torrentio API errors."""
