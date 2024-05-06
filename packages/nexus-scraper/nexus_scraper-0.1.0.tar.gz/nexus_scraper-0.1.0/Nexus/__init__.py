"""
Welcome to Nexus!

Nexus is a Python package that provides a simple interface for scraping torrent sites and aggregating the results.

This package is designed to be used with Jackett, Prowlarr, Torbox, Torrentio, and Annatar, but can be extended to support other sources.

The main components of Nexus are:
- `Nexus`: The main class that provides an interface for scraping torrent sites.
- `ScrapeResult`: A data class that represents a single scrape result.
- `NexusSettings`: A data class that stores Nexus settings.
- `annatar`: A scraper for Annatar.
- `jackett`: A scraper for Jackett.
- `prowlarr`: A scraper for Prowlarr.
- `torbox`: A scraper for Torbox.
- `torrentio`: A scraper for Torrentio.

To get started, you can create a `Nexus` instance and use the `scrape` method to search for torrents.

For example:
```python
from Nexus import Nexus

nexus = Nexus()
results = nexus.scrape(source="torrentio", query="ubuntu")
for result in results:
    print(result)
```

This will search for torrents matching the query "ubuntu" on Torrentio and print the results.
"""

import Nexus
from Nexus import exceptions, models, scraper
from Nexus.models import NexusSettings, ScrapeResult
from Nexus.scrapers import (
    annatar,
    jackett,
    orionoid,
    prowlarr,
    torbox,
    torrentio,
)

__all__ = [
    "Nexus",
    "ScrapeResult",
    "NexusSettings",
    # Modules
    "scraper",
    "models",
    "exceptions",
    # Scrapers
    "annatar",
    "jackett",
    "orionoid",
    "prowlarr",
    "torbox",
    "torrentio"
]