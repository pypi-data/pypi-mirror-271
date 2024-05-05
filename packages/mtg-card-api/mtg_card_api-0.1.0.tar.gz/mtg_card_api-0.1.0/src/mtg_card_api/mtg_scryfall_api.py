import logging
import os
from pathlib import Path
import jsonpickle
from diskcache import Cache

from rest_client_micro import Response as R
from rest_client_micro import RESTClient as RC
from rest_client_micro import RESTObject as RO


class ScryfallAPI():

    app_name: str = 'MTGScryfallAPI'
    sleep_ms: int = 1000
    cache_time_mins: int = 1440
    cache: Cache
    cache_dir: str
    config_dir: str
    use_cache: bool
    force_cache: bool
    user_agent: str = 'MTG-Card-API/0.1 (https://github.com/samuelshiels/MTG-Card-API)'
    root_url: str = 'https://api.scryfall.com/'

    logging.basicConfig(
        format='%(asctime)s | %(levelname)s | %(message)s', level=logging.DEBUG)
    debug: bool = False

    def _debug(self, message: str):
        if self.debug:
            logging.debug(str(message))

    def __init__(self,
            config_dir: str = None,
            cache_dir: str = None,
            cache_refresh_mins: int = 1440,
            force_cache: bool = False,
            use_cache: bool = True) -> None:
        self.config_dir = config_dir or os.path.join(
            str(Path.home()), ".config/", self.app_name)
        self.cache_dir = cache_dir or os.path.join(
            str(Path.home()), ".cache/", self.app_name)
        self.cache_time_mins = cache_refresh_mins
        self.force_cache = force_cache
        self.use_cache = use_cache
        self.cache = Cache(self.cache_dir)

    def _build_header_obj(self) -> dict:
        headers = {}
        headers['User-Agent'] = self.user_agent
        # we want responses in json, because fuck xml
        headers['Accept'] = 'application/json'
        return headers

    def run(self):
        pass
