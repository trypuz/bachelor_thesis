import pysolr


def connect_to_platform(url):
    solr = pysolr.Solr(url, always_commit=True)
    solr.ping()
    return solr

