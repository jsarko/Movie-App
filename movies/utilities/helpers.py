import re, requests

from bs4 import BeautifulSoup

from consts import HEADERS

def getPageSoup(url: str) -> BeautifulSoup:
    rs = requests.get(url, headers=HEADERS)
    return BeautifulSoup(rs.text, "html.parser")

def getRarbgMagnetLink(torrentUrl):
    # Returns the magnet link for the specified
    # torrent.
    return ""

def extractRarbgDetails(item: BeautifulSoup) -> dict:
    details = {}
    name_tag = item.select('.name')[0].find_all(
        href=re.compile("/torrent")
    )
    seed_tag = item.select('.seeds')
    size_tag = item.select('.size')

    # If theres no name we probably dont want it
    if not name_tag:
        return None
    
    link = name_tag[0].get('href')
    
    # Build details dict
    details['name'] = (name_tag[0].get_text())
    details['seeds'] = seed_tag[0].get_text()
    details['size'] = size_tag[0].get_text()
    details['magnet_link'] = getRarbgMagnetLink(link)
    return details