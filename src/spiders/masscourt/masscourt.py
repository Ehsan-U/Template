from typing import Dict, List

from src.drivers import PlaywrightDriver
from src.interfaces import Client, Exporter, Notifier, Spider
from src.utils import logger



class MassCourt(Spider):
    name = "masscourt"
    
    
    def __init__(self, client: Client, driver: PlaywrightDriver, exporter: Exporter, notifier: Notifier) -> None:
        self.client = client
        self.driver = driver
        self.exporter = exporter
        self.notifier = notifier


    @classmethod
    def create_spider(cls, client: Client, driver: PlaywrightDriver, exporter: Exporter, notifier: Notifier) -> "MassCourt":
        return cls(
            client=client,
            driver=driver,
            exporter=exporter,
            notifier=notifier,
        )
    

    def crawl(self) -> List[Dict]:
        logger.info(f"Starting crawl for {self.name}")
        self.client.fetch(url="https://books.toscrape.com", method="GET")
        self.driver.get_page("https://books.toscrape.com")
        self.exporter.export([{"name": self.name}])
        self.notifier.notify("Hello", ['John Doe'])
        logger.info(f"Finished crawl for {self.name}")
        return [{}]
