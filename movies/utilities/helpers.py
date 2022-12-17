import re, requests
from urllib.parse import quote

from bs4 import BeautifulSoup

from movies.consts import HEADERS, BASE_URL_1337x

def getPageSoup(url: str) -> BeautifulSoup:
    rs = requests.get(url, headers=HEADERS)
    return BeautifulSoup(rs.text, "html.parser")

def get1337xSearchUrl(title: str) -> str:
    return f'{BASE_URL_1337x}/search/{quote(title)}/1/'

def get1337xMagnetLink(torrentUrl):
    # Returns the magnet link for the specified
    # torrent.
    soup = getPageSoup(BASE_URL_1337x + torrentUrl)
    magnet = soup.select_one("a[href*=magnet]").get('href')
    return magnet

def extract1337xDetails(item: BeautifulSoup) -> dict:
    details = {}
    name_tag = item.select('.name')[0].find_all(
        href=re.compile("/torrent")
    )
    seed_tag = item.select('.seeds')
    size_tag = item.select('.size')

    # If theres no name we probably dont want it
    if not name_tag:
        return None
    
    # Build details dict
    details['name'] = (name_tag[0].get_text())
    details['seeds'] = seed_tag[0].get_text()
    details['size'] = size_tag[0].get_text()
    details['torrent_url'] = name_tag[0].get('href')
    return details