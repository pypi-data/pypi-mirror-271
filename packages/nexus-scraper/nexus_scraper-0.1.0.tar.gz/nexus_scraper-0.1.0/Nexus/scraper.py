import concurrent.futures
from typing import List

from Nexus.exceptions import NexusException
from Nexus.models import NexusSettings, ScrapeResult
from Nexus.scrapers.annatar import Annatar
from Nexus.scrapers.jackett import Jackett
from Nexus.scrapers.orionoid import Orionoid
from Nexus.scrapers.prowlarr import Prowlarr
from Nexus.scrapers.torbox import TorBox
from Nexus.scrapers.torrentio import Torrentio


class NexusScrapers:
    def __init__(self, settings: NexusSettings):
        self.settings = settings
        self.scrapers = {
            "annatar": Annatar(),
            "jackett": Jackett(settings),
            "torbox": TorBox(),
            "orionoid": Orionoid(settings),
            "prowlarr": Prowlarr(settings),
            "torrentio": Torrentio()
        }

    def scrape(self, source, query, **kwargs) -> List[ScrapeResult]:
        """Scrape a source for a query."""
        if source not in self.scrapers:
            return self.scrapers["torrentio"].scrape(query, **kwargs)
        return self.scrapers[source].scrape(query, **kwargs)

    def scrape_all(self, query="", **kwargs) -> List[ScrapeResult]:
        """Scrape all sources for a query."""
        results = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            scrape_tasks = {executor.submit(self.scrape, source, query, **kwargs): source for source in self.scrapers}
            for future in concurrent.futures.as_completed(scrape_tasks):
                source = scrape_tasks[future]
                try:
                    result = future.result()
                    results.extend(result)
                    # print(f"Scraped {len(result)} items from {source}")
                except Exception as e:
                    raise NexusException(f"Error scraping from {source}: {str(e)}")
        return results

    def get_sources(self):
        """Get a list of available sources."""
        return list(self.scrapers.keys())

    def get_scraper(self, source):
        """Get a scraper by source."""
        if source not in self.scrapers:
            return self.scrapers["torrentio"]
        return self.scrapers[source]
