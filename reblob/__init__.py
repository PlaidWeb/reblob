""" reblob functions """

import urllib.parse
import re

from bs4 import BeautifulSoup
import requests
import pypandoc

__version__ = '0.0.0'


def _get_articles(soup):
    return (soup.find_all(class_="e-content")
            or soup.find_all(class_="h-entry")
            or soup.find_all("article")
            or soup.find_all(class_="entry")
            or [soup])


def _rewrite_srcset(srcset, base_url):
    parts = srcset.split(',')
    out_parts = []
    for part in parts:
        url, *other = part.split()
        url = urllib.parse.urljoin(base_url, url)
        out_parts.append(' '.join([url, *other]))
    return ', '.join(out_parts)


def convert_text(doc, base_url, format='markdown_github'):
    """ Convert a BeautifulSoup document to output markup; attempts to find
    a plausible article to excerpt.

    Arguments:

    doc -- the BeautifulSoup document object

    base_url -- the base URL of the original document

    format -- the output format to use; uses anything supported by Pandoc

    Returns: the converted document fragment
    """

    articles = _get_articles(doc)

    title = doc.find('title').decode_contents()

    out_html = '<p><a href="{url}">{title}</a>:</p>\n'.format(
        url=base_url, title=title)

    for article in articles:
        # convert all href, src, and srcset attributes
        for attr in ('href', 'src'):
            for node in article.findAll(**{attr: True}):
                node[attr] = urllib.parse.urljoin(base_url, node[attr])
        for node in article.findAll(srcset=True):
            node['srcset'] = _rewrite_srcset(node['srcset'], base_url)

        out_html += '<blockquote>' + article.decode_contents() + '</blockquote>\n'

    return pypandoc.convert_text(out_html, format, 'html')


def convert(url, format='markdown_github'):
    """ Given a URL, make an entry file.

    Arguments:

    url -- the URL of the document

    format -- the content format of the document
    """

    r = requests.get(url)
    if not 200 <= r.status_code < 300:
        r.raise_for_status()
    return convert_text(BeautifulSoup(r.text, features='html.parser'), r.url, format)
