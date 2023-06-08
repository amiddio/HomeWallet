import requests

from abc import ABC, abstractmethod
from bs4 import BeautifulSoup


class ParserBase(ABC):

    __headers = ({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'text/html; charset=utf-8',
    })

    def get_headers(self) -> dict[str, str]:
        return self.__headers

    def get_html_parser(self, url: str) -> BeautifulSoup:
        webpage = requests.get(url, headers=self.get_headers())
        return BeautifulSoup(webpage.text, "html.parser")

    @staticmethod
    def currency_convert(value: float, factor: float) -> float:
        return round(value * factor, 2)

    @abstractmethod
    def parse_usd_gel(self) -> str | None:
        pass

    @abstractmethod
    def parse_gel_usd(self) -> str | None:
        pass
