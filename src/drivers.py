from playwright.sync_api import BrowserContext, BrowserType, Page, Playwright, Frame, Route, Request
from urllib.parse import urlparse
from parsel import Selector
from typing import Dict

from src.utils import logger
from src.models import ElementSelector



class PlaywrightDriver:
    """ Playwright with wrappers """


    def __init__(self, context: BrowserContext, page: Page, timeout: int) -> None:
        self.context = context
        self.page = page
        self.timeout = timeout

    
    @classmethod
    def create_driver(
        cls,
        playwright: Playwright,
        browser_launch_type: str,
        launch_args: Dict,
        global_timeout: int = 30*1000,
    ) -> "PlaywrightDriver":
        browser_type : BrowserType = getattr(playwright, browser_launch_type)
        browser = browser_type.launch(**launch_args)
        context = browser.new_context()
        page = context.new_page()
        driver = cls(context, page, global_timeout)
        return driver
    

    def exists(self, el: ElementSelector, iframe: Frame = None) -> bool:
        target = iframe if iframe else self.page
        action_name = f"{self.__class__.__name__}.{self.exists.__name__}"
        try:
            logger.debug(f"Attempting to find selector '{el.name}' in {'iframe' if iframe else 'page'}")
            count = target.locator(selector=el.value).count()
            exists = count > 0
            logger.debug(f"Selector '{el.name}' {'exists' if exists else 'does not exist'} (count: {count})")
            return exists
        except Exception as e:
            logger.error(f"Error in '{action_name}' for selector '{el.name}': {str(e)}")
            return False
    

    def click(self, el: ElementSelector, wait_after: int = None, iframe: Frame = None, timeout: int = None) -> bool:
        target = iframe if iframe else self.page
        action_name = f"{self.__class__.__name__}.{self.click.__name__}"
        try:
            logger.debug(f"Attempting to click selector '{el.name}' in {'iframe' if iframe else 'page'}")
            timeout = self.timeout if timeout is None else timeout
            target.click(selector=el.value, timeout=timeout)
            if wait_after is not None:
                target.wait_for_timeout(wait_after)
            logger.debug(f"Selector '{el.name}' clicked")
            return True
        except Exception as e:
            logger.error(f"Error in '{action_name}' for selector '{el.name}': {str(e)}")
            return False

    
    def fill(self, el: ElementSelector, value: str, wait_after: int = None, iframe: Frame = None, timeout: int = None) -> bool:
        target = iframe if iframe else self.page
        action_name = f"{self.__class__.__name__}.{self.fill.__name__}"
        try:
            logger.debug(f"Attempting to fill selector '{el.name}' in {'iframe' if iframe else 'page'}")
            timeout = self.timeout if timeout is None else timeout
            target.fill(selector=el.value, value=value, timeout=timeout)
            if wait_after is not None:
                target.wait_for_timeout(wait_after)
            logger.debug(f"Selector '{el.name}' filled")
            return True
        except Exception as e:
            logger.error(f"Error in '{action_name}' for selector '{el.name}': {str(e)}")
            return False


    def wait_for_selector(self, el: ElementSelector, state: str = "visible", iframe: Frame = None, timeout: int = None) -> bool:
        target = iframe if iframe else self.page
        action_name = f"{self.__class__.__name__}.{self.wait_for_selector.__name__}"
        try:
            logger.debug(f"Attempting to wait for '{el.name}' in {'iframe' if iframe else 'page'}")
            timeout = self.timeout if timeout is None else timeout
            target.wait_for_selector(selector=el.value, timeout=timeout, state=state)
            logger.debug(f"Selector '{el.name}' found (state: {state})")
            return True
        except Exception as e:
            logger.error(f"Error in '{action_name}' for selector '{el.name}': {str(e)}")
            return False

    
    def get_page(self, url: str, wait_el: ElementSelector = None, wait_after: int = 0, wait_until: str = "load", timeout: int = None) -> str:
        target = self.page
        action_name = f"{self.__class__.__name__}.{self.get_page.__name__}"
        try:
            logger.debug(f"Attempting to navigate to '{url}'")
            timeout = self.timeout if timeout is None else timeout
            target.goto(url, timeout=timeout, wait_until=wait_until)
            if wait_el:
                self.wait_for_selector(el=wait_el, timeout=timeout)
            if wait_after:
                target.wait_for_timeout(wait_after)
            logger.debug(f"Successfully navigated to '{url}'")
            response = target.content()
            return response
        except Exception as e:
            logger.error(f"Error in '{action_name}' for URL '{url}': {str(e)}")
            return None
    

    def selector(self, iframe: Frame = None) -> Selector:
        target = iframe if iframe else self.page
        content = target.content()
        return Selector(text=content)
    
    
    def block_resources(self, route: Route, request: Request):
        ad_domains = ['googletagmanager.com']
        request_domain = urlparse(request.url)
        if request.resource_type == "image" or any([domain for domain in ad_domains if domain in request_domain]):
            route.abort()
        else:
            route.continue_()


    def close(self) -> None:
        action_name = f"{self.__class__.__name__}.{self.close.__name__}"
        if hasattr(self, "browser"):
            try:
                self.context.close()
                logger.debug(f"Browser closed")
            except Exception as e:
                logger.error(f"Error in '{action_name}': {str(e)}")
