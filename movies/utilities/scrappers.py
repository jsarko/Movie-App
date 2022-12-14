from helpers import getPageSoup, extractRarbgDetails

class Scraper:
    def __init__(self, url: str):
        self.soup = getPageSoup(url)
    
    def get_list_by_url(self) -> list:
        pass
    
    def list(self, limit=5) -> list:
        return self.get_listset()[:limit]

class RargbScrapper(Scraper):
    def get_listset(self) -> list:
        ls = []
        for item in self.soup.find_all("tr"):
            details = extractRarbgDetails(item)
            if details:    
                ls.append(details)
        return ls

# Avoiding detection
# https://www.zenrows.com/blog/stealth-web-scraping-in-python-avoid-blocking-like-a-ninja#rotating-proxies

print(RargbScrapper("https://www.1377x.to/search/The%20Irishman/1/").list())
