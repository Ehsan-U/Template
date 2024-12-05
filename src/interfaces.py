from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from src.models import TextResponse
from src.drivers import PlaywrightDriver



class Exporter(ABC):
    """ Interface for creating exporters """


    @classmethod
    @abstractmethod 
    def create_exporter(cls, filename: str) -> "Exporter":
        ...


    @abstractmethod 
    def export(self, items: List[Dict]):
        ...
    

    @abstractmethod 
    def close(self):
        ...


class Notifier(ABC):
    """ Interface for creating notifiers """


    @classmethod
    @abstractmethod 
    def create_notifier(cls) -> "Notifier":
        ...


    @abstractmethod 
    def notify(self, msg: str, recipients: List[str]):
        ...


class Client(ABC):
    """ Interface for creating HTTP clients """
    name: str

    
    @classmethod
    @abstractmethod
    def create_client(cls) -> "Client":
        return cls()
    
    
    @abstractmethod
    def fetch(self, url: str, method: str, **kwargs) -> TextResponse:
        ...


class Spider(ABC):
    """ Interface for creating spiders """
    name: str


    @classmethod
    @abstractmethod 
    def create_spider(
        cls,
        client: Client,
        driver: PlaywrightDriver,
        exporter: Exporter,
        notifier: Notifier,
        # sometime one spider dependent on other
        # dependent_spider: Optional['Spider'] = None
    ) -> "Spider":
        ...


    @abstractmethod 
    def crawl(self) -> List[Dict]:
        ...
