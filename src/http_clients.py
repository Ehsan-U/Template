from curl_cffi.requests import Session

from src.interfaces import Client
from src.models import TextResponse
from src.utils import logger



class CurlCffi(Client):
    name = "curl_cffi"
    

    def __init__(self) -> None:
        self.session = Session()
            
    
    @classmethod
    def create_client(cls) -> "CurlCffi":
        return cls()


    def fetch(self, url: str, method: str = "GET", **kwargs) -> TextResponse:
        try:
            response = self.session.request(
                url=url,
                method=method,
                **kwargs,
            )
            logger.debug(f"Got ({response.status_code}) <{method.upper()} {url}> ({self.name})")
            response.raise_for_status()
        except Exception as e:
            logger.error(f"Error while fetching: {e}")
            return TextResponse(
                url=url,
                status_code=0,
                text="",
                headers={},
                error_msg=str(e)
            )
        else:
            return TextResponse(
                url=response.url,
                status_code=response.status_code,
                text=response.text,
                headers={k:v for k,v in response.headers.items()}
            )
