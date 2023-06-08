import re
from parser.currency.parser_base import ParserBase
from bs4 import BeautifulSoup


class Pokur(ParserBase):

    URL_GEL_USD = 'https://pokur.su/gel/usd/1/'
    URL_USD_GEL = 'https://pokur.su/usd/gel/1/'

    def _parse(self, url: str):
        soup: BeautifulSoup = self.get_html_parser(url)
        if not soup:
            return

        res = soup.find('div', class_='blockquote-classic').findNext()
        if res:
            value = re.search(r'\s(\d+[,|\.]\d+)\s', res.text)
            if value:
                value = value.group().strip().replace(',', '.')
                return float(value)

    def parse_usd_gel(self) -> float | None:
        return self._parse(url=Pokur.URL_USD_GEL)

    def parse_gel_usd(self) -> float | None:
        return self._parse(url=Pokur.URL_GEL_USD)
