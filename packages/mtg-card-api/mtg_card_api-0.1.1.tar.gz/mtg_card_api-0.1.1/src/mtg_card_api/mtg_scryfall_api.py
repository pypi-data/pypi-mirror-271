import logging
import os
from pathlib import Path
import jsonpickle
from diskcache import Cache
from rest_client_micro import Response as R
from rest_client_micro import RESTClient as RC
from rest_client_micro import RESTObject as RO
from . import _utils as Utils


class ScryfallAPI():

    app_name: str = 'MTGScryfallAPI'
    sleep_ms: int = 100
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

    def _run_get(self, e: str, p: dict, o: str, c) -> R:
        if self.force_cache:
            return self._run_rest(e, p, o, c)

        if self.use_cache:
            cache_result = self.cache.get(o)
            if cache_result is not None:
                return cache_result
            else:
                return self._run_rest(e, p, o, c)

    def _run_rest(self, e: str, p: dict, o: str, c) -> R:
        self._debug("__runRest")
        rc = RC()
        rc.sleep_ms = self.sleep_ms
        rest_obj = RO(operation='get', endpoint=f'{self.root_url}{e}',
                      params=p, headers=self._build_header_obj(), payload={})
        config = {}
        config['output'] = o + '.json'
        config['cache'] = self.cache_dir + c
        config['time'] = self.cache_time_mins
        config['sleep'] = self.sleep_ms
        config['rest'] = rest_obj
        self._debug(f"{config}")
        response = rc.execute(rest_obj)
        if self.use_cache:
            self._set_cache(o, response)

        return response

    def clear_cache(self) -> None:
        """
        Clears all keys from the diskcache database
        """
        self.cache.clear()

    def _set_cache(self, key: str, response: R) -> None:
        if response.error is False:
            thawed = jsonpickle.decode(response.response)
            if 'error' not in thawed:
                self.cache.set(
                    key=key,
                    value=response,
                    expire=self.cache_time_mins*60)

    def get_card_by_name(self, card_name: str) -> R:
        """Searches Scryfall by the exact name

        Args:
            card_name (str): Exact string oracle english name of a card, case insensitive

        Returns:
            R: Full card object https://scryfall.com/docs/api/cards
        """
        return self._run_get(
            'cards/named',
            {
                'exact': card_name
            },
            Utils.encodeMD5(card_name),
            'cache/cards')

    def run(self):
        pass
