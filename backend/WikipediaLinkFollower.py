import requests
import logging
from bs4 import BeautifulSoup, NavigableString, Comment
from urllib.parse import urljoin, urlparse
from collections import OrderedDict

from errors import LinkLoopError, PageMissingError, PageWithoutLinkError


def follow_between(start_url, goal_url):
    """Starting at start_url, follow wikipedia links until goal_url is reached"""
    visited = OrderedDict()
    current_url = start_url
    while True:
        logging.info(f"Visiting {current_url}")

        if current_url in visited:
            raise LinkLoopError(current_url, visited)

        # Fetch url contents and look for a next link
        r = requests.get(current_url)
        if r.status_code == 404:
            raise PageMissingError(current_url, visited)

        # Parse page contents
        soup = BeautifulSoup(r.content, "html.parser")
        page_main = soup.find("div", {"role": "main"})
        assert page_main, "Wikipedia page has no role:main div"

        next_url = get_first_valid_link(current_url, page_main)
        if next_url is None:
            raise PageWithoutLinkError(current_url, visited)

        # Mark as visited and recurse
        visited[current_url] = get_page_info(current_url, page_main)

        if current_url == goal_url:
            return list(visited.values())
        current_url = next_url.lower()


def is_tag_italicized(tag):
    """Return wether a tag in a wikipedia article produces italicized contents"""
    return tag.name == "i" or (
        tag.name == "div" and "role" in tag.attrs and tag.attrs["role"] == "note"
    )


def find_non_italicized_parenthesized_links(paragraph):
    """Traverse a paragraph and yield links that are not inside parenthesis
    and not inside an italicized element"""
    parenthesis = 0

    def traverse(tag):
        nonlocal parenthesis
        if isinstance(tag, NavigableString) and not isinstance(tag, Comment):
            parenthesis += tag.count("(") - tag.count(")")
            if parenthesis < 0:
                logging.warning("Missing parenthesis in article.")
                parenthesis = 0
        elif tag.name == "a" and parenthesis == 0:
            yield tag
        elif not is_tag_italicized(tag):
            for child in tag.children:
                yield from traverse(child)

    yield from traverse(paragraph)


DEFAULT_THUMBIMAGE = (
    "https://www.wikipedia.org/portal/wikipedia.org/assets/img/Wikipedia-logo-v2.png"
)
NB_READ_PARAGRAPHS = 15


def get_page_info(page_url, page_main):
    """Return a title, image, and text from the wikipedia page content in order to create a thumbnail"""
    all_text = "".join(p.text for p in page_main.find_all("p")[:NB_READ_PARAGRAPHS])
    all_thumbimages = page_main.select("img.thumbimage")
    return {
        "title": page_main.select("h1")[0].text.strip(),
        "image": all_thumbimages[0].attrs["src"]
        if all_thumbimages
        else DEFAULT_THUMBIMAGE,
        "text": all_text[:250] + "...",
        "url": page_url,
    }


def get_first_valid_link(page_url, page_main):
    """Get the first link of a wikipedia page, ignoring external links,
    links to the current page, or red links (links to non-existent pages)"""

    # Save page url parts for comparison
    page_url_parts = urlparse(page_url)
    assert page_url_parts.hostname.endswith(
        ".wikipedia.org"
    ), "A wikipedia.org page is expected"
    assert len(page_main.select("p > p")) == 0, "There should not be nested <p> tags"

    for paragraph in page_main.find_all("p"):
        for link in find_non_italicized_parenthesized_links(paragraph):
            if "href" not in link.attrs:
                continue

            # Transform relative URLs to absolute URLs with urljoin
            link_url = urljoin(page_url_parts.geturl(), link.attrs["href"])
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
            if ":" in link_url_parts.path:
                continue

            return link_url

    return None
