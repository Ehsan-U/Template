from functools import cached_property
from enum import Enum
from parsel import Selector, SelectorList
from dataclasses import dataclass 
from typing import Dict, Optional



class ElementSelector(Enum):
    """
    Represents an element within an HTML page structure.

    Each element has two attributes:

    * `name`: A string representing the user-defined name for the selector.
    * `value`: A string representing the element's location within the HTML structure,
              often expressed as a CSS or XPATH selector.

    """



@dataclass
class TextResponse:
    url: str
    status_code: int
    headers: Dict
    text: str
    error_msg: Optional[str] = None

    
    # python ^3.8
    @cached_property
    def selector(self) -> Selector:
        return Selector(text=self.text)


    def xpath(self, query: str) -> SelectorList[Selector]:
        return self.selector.xpath(query)
