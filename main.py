from playwright.sync_api import sync_playwright 

from src.http_clients import CurlCffi
from src.spiders.masscourt import MassCourt
from src.drivers import PlaywrightDriver
from src.extensions import CsvExporter, EmailNotifier


###### dependencies ########
driver = PlaywrightDriver.create_driver(
    playwright=sync_playwright().start(),
    browser_launch_type="firefox",
    launch_args={
        "headless": False,
    }
)
exporter = CsvExporter.create_exporter("output.csv")
notifier = EmailNotifier.create_notifier()
client = CurlCffi.create_client()


##### spiders #####
masscourt_spider = MassCourt.create_spider(
    client=client,
    driver=driver,
    exporter=exporter,
    notifier=notifier,
)
masscourt_spider.crawl()
