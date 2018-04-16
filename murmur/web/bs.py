"""Parse google search page and pick up articles."""

import requests
from bs4 import BeautifulSoup
import random
from datetime import datetime, timedelta


def random_date(old_year=10):
    """Get random datetime for this old_year[year]."""
    td_unix = random.randint(0, old_year * 3600 * 24 * 365)
    td = timedelta(seconds=td_unix)
    return datetime.now() - td


class Parser():
    """Parser client."""

    def __init__(self):
        """Set parameters."""
        pass

    def create_soup_from_url(self, url):
        """Request data with url and return bs instance."""
        res = requests.get(url)
        # res.encoding = "utf-8"
        soup = BeautifulSoup(res.text, "html5lib")
        # print(res.text)
        return soup

    def scrape_articles_google(self, soup):
        """Scrape google search result."""
        articles = soup.find_all(class_="g")
        results = []
        for article in articles:
            # print(article)
            try:
                title = article.find("h3").a.text
                url = article.find("cite").text
                content = article.find("span", class_="st").text
                content = content.split(" ... ")[1].replace("\n", "")
                # print()
                # print(title)
                # print(url)
                # print(content)
                results.append({
                    "title": title,
                    "url": url,
                    "date": random_date().strftime("%Y/%m/%d"),
                    "content": content,
                })
            except:
                pass
        return results

if __name__ == "__main__":

    url = ("https://www.google.co.jp/search?q={}"
           "&oq=ruby+on+rails&aqs=chrome..69i57j69i64.11678j0j1"
           "&sourceid=chrome&ie=UTF-8")
    url = url.format("ruby+on+rails+tutorial")
    parser = Parser()
    soup = parser.create_soup_from_url(url)
    parser.scrape_articles_google(soup)
