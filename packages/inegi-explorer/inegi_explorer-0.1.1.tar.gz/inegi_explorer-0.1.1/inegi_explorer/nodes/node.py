import concurrent.futures
import json
import re
import urllib.request
from abc import ABC, abstractmethod

from typing import List, Union

import pandas as pd
import warnings

warnings.filterwarnings("ignore", category=UserWarning)


class Node(ABC):
    type: str

    def __init__(self, name: str,
                 series_key: str,
                 database: int,
                 data: dict,
                 geographic_area: str = "0700", geographic_area_name: str = "Estados Unidos Mexicanos"):
        self.name: str = name
        self.series_key: str = series_key
        self.database: int = database
        self.data: dict = data
        self.geographic_area: str = geographic_area
        self.geographic_area_name: str = geographic_area_name
        self._children: Union[list, None] = []

    def __repr__(self) -> str:
        if children := self.get_children():
            return f"{self.type}: {self.name} - {self.geographic_area_name} ({self.id}) \n    " \
                + "\n    ".join(
                    [f"{child.type}: {child.name} - {child.geographic_area_name} ({child.id})" for child in children])

        else:
            return f"{self.type}: {self.name} - {self.geographic_area_name} ({self.id})"

    def __getitem__(self, item):
        return self.get_children().__getitem__(item)

    @property
    def id(self) -> str:
        return f"{self.type[0]}-{self.geographic_area}-{self.series_key}-{self.database}"

    @property
    @abstractmethod
    def url_children(self) -> str:
        pass

    @abstractmethod
    def get_children(self) -> Union[List[Union['Node', None]], None]:
        pass

    @abstractmethod
    def fetch(self, raw: bool = False, *args, **kwargs) -> Union[pd.DataFrame, pd.Series, dict, List[dict]]:
        pass

    @classmethod
    @abstractmethod
    def from_response(cls, response: dict) -> 'Node':
        pass

    @staticmethod
    def request_url(url: str, debug=False) -> Union[list, dict]:
        data = urllib.request.urlopen(url).read()
        if debug:
            print(f"Requested: {url}")
            print(f"Recieved: {data}")
        decoded = re.sub(r'\\u000d\\u000a|\\u000d|\\u000a|\xa0', ' ', data.decode("utf-8"))
        return json.loads(decoded)

    @staticmethod
    def request_urls(urls: list[str], debug=False, parsing: callable = lambda x: x) -> list:
        def req(url):
            return Node.request_url(url, debug)

        with concurrent.futures.ThreadPoolExecutor(max_workers=None) as executor:
            futures = [executor.submit(req, url) for url in urls]
            series_list = [parsing(future.result()) for future in futures]
        return series_list
