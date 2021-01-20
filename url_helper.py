from urllib import request


def get_source_from_url(url):
    response = request.urlopen(url)
    page_source = response.read().decode('utf-8')
    return page_source
