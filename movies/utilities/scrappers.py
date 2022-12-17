from movies.utilities.helpers import getPageSoup, extract1337xDetails

class Scraper:
    def __init__(self, url: str):
        self.soup = getPageSoup(url)
    
    def get_list_by_url(self) -> list:
        pass
    
    def list(self, limit=5) -> list:
        return self.get_listset()[:limit]

class Scrapper1337x(Scraper):
    def get_listset(self) -> list:
        ls = []
        for item in self.soup.find_all("tr"):
            details = extract1337xDetails(item)
            if details:    
                ls.append(details)
        return ls

# Avoiding detection
# https://www.zenrows.com/blog/stealth-web-scraping-in-python-avoid-blocking-like-a-ninja#rotating-proxies