from typing import List, Dict
import csv

from src.interfaces import Exporter, Notifier
from src.utils import logger



class CsvExporter(Exporter):
    

    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.file = open(self.filename, mode='w')


    @classmethod
    def create_exporter(cls, filename: str) -> "CsvExporter":
        return cls(filename)

    
    def export(self, items: List[Dict]):
        try:
            if not items:
                logger.info("Nothing to export!")
                return
            writer = csv.DictWriter(
                f=self.file,
                fieldnames=items[0].keys(),
            )
            writer.writerows(items)
        except Exception as e:
            logger.error(f"Error while exporting items to {self.filename}: {e}")

    
    def close(self):
        try:
            self.file.close()
        except Exception as e:
            logger.error(f"Error while closing {self.filename}: {e}")



class EmailNotifier(Notifier):
    
    
    def __init__(self) -> None:
        pass


    @classmethod
    def create_notifier(cls) -> "EmailNotifier":
        return cls()

    
    def notify(self, msg: str, recipients: List[str]):
        for recipient in recipients:
            logger.info(f"[Email] \nMessage: {msg}\nRecipient: {recipient}")
