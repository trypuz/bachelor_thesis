import urllib.error
import logging
import socket
from urllib import request
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def get_source_from_url(url):
    try:
        response = request.urlopen(url)
        page_source = response.read().decode('utf-8')
        return page_source
    except urllib.error.URLError as e:
        if isinstance(e.reason, socket.timeout):
            logger.error(f"Error during fetching page source with url {url}")
            pass


def convert_source_to_soup(page_source):
    soup_handler = BeautifulSoup(page_source, "html.parser")
    return soup_handler
