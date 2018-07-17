import requests
import logging
from bs4 import BeautifulSoup, NavigableString, Comment
from urllib.parse import urljoin, urlparse


class LinkLoopError(Exception):
    pass


class PageMissingError(Exception):
    pass


class PageWithoutLinkError(Exception):
    pass


class WikipediaLinkFollower:
    def __init__(self, start_url, goal_url):
        self.current_url = start_url
        self.goal_url = goal_url
        self.visited = {}
        logging.info(f"Starting at {self.current_url}")
        while self.has_next():
            logging.info(f"STOP BY {self.current_url}")

    def has_next(self):
        if self.current_url == self.goal_url:
            return False

        if self.current_url in self.visited:
            raise LinkLoopError()

        # Fetch url contents and look for a next link
        r = requests.get(self.current_url)
        if r.status_code == 404:
            raise PageMissingError()

        next_url = self.get_first_valid_link(self.current_url, r.content)
        if next_url is None:
            raise PageWithoutLinkError()

        # Move to the next url and return
        self.visited[self.current_url] = True
        self.current_url = next_url
        return True

    @classmethod
    def is_wikipedia_tag_italicized(cls, tag):
        """Return wether a tag in a wikipedia article produces italicized contents"""
        return tag.name == "i" or (tag.name == "div" and "role" in tag.attrs and tag.attrs["role"] == "note")

    @classmethod
    def find_non_italicized_parenthesized_links(cls, paragraph):
        parenthesis = 0

        def traverse(tag):
            nonlocal parenthesis
            if isinstance(tag, NavigableString) and not isinstance(tag, Comment):
                parenthesis += tag.count('(') - tag.count(')')
                if parenthesis < 0:
                    logging.warning("Missing parenthesis in article.")
                    parenthesis = 0
            elif tag.name == "a" and parenthesis == 0:
                yield tag
            elif not cls.is_wikipedia_tag_italicized(tag):
                for child in tag.children:
                    yield from traverse(child)

        yield from traverse(paragraph)

    @classmethod
    def get_first_valid_link(cls, page_url, page_content):
        """Get the first link of a wikipedia page, ignoring external links,
        links to the current page, or red links (links to non-existent pages)"""
        soup = BeautifulSoup(page_content, "html.parser")
        page_main = soup.find("div", {"role": "main"})
        if not page_main:
            logging.error(f"Cannot find the main content div for page {page_url}")
            return None

        # Save page url parts for comparison
        page_url_parts = urlparse(page_url)
        assert page_url_parts.hostname.endswith(".wikipedia.org"), "A wikipedia.org page is expected"
        assert len(page_main.select("p > p")) == 0, "There should not be nested <p> tags"

        for paragraph in page_main.find_all("p"):
            for link in cls.find_non_italicized_parenthesized_links(paragraph):
                if 'href' not in link.attrs:
                    continue

                # Transform relative URLs to absolute URLs with urljoin
                link_url = urljoin(page_url_parts.geturl(), link.attrs['href'])
                link_url_parts = urlparse(link_url)

                # Reject links with a different Wikipedia hostname
                if link_url_parts.hostname != page_url_parts.hostname:
                    continue

                # Reject links that don't go to a wiki
                if not link_url_parts.path.startswith("/wiki/"):
                    continue

                # Reject links to same page
                if link_url_parts.path == page_url_parts.path:
                    continue

                # Reject Wikipedia meta links that contain a solon
                if ':' in link_url_parts.path:
                    continue

                return link_url

        return None