""" reblob functions """

import urllib.parse
import logging

from bs4 import BeautifulSoup
import requests
import mf2py
import pypandoc

from . import dom_extract


LOGGER = logging.getLogger('reblob')


def _rewrite_srcset(srcset, base_url):
    parts = srcset.split(',')
    out_parts = []
    for part in parts:
        url, *other = part.split()
        url = urllib.parse.urljoin(base_url, url)
        out_parts.append(' '.join([url, *other]))
    return ', '.join(out_parts)


def _extract_mf(item, base_url):
    """ Convert an mf2-formatted entry to a pretty blockquote """
    properties = item.get('properties', {})

    out_html = '<p>'

    if 'author' in properties:
        # just use the primary author for now
        author = properties.get('author')[0].get('properties', {})

        if 'url' in author and 'name' in author:
            out_html += '<a href="{url}">{name}</a>: '.format(
                url=author.get('url')[0],
                name=author.get('name')[0])
        elif 'name' in author:
            out_html += '{name}: '.format(name=author.get('name')[0])

    if 'url' in properties:
        url = properties['url'][0]
    else:
        url = base_url

    if 'name' in properties:
        title = properties['name'][0]
    else:
        title = base_url

    out_html += '<a href="{url}">{title}</a>:'.format(url=url, title=title)

    out_html += '</p>'

    out_html += '<blockquote cite="{url}">'.format(url=url)

    if 'content' in properties:
        for content in properties['content']:
            if 'html' in content:
                out_html += content['html']
            elif 'value' in content:
                out_html += '\n'.join(
                    ['<p>%s</p>' % para
                     for para in content['value'].split('\n')])
    elif 'summary' in properties:
        out_html += '\n'.join(['<p>%s</p>' %
                               summary for summary in properties['summary']])

    out_html += '</blockquote>'
    return out_html


def _extract_dom(dom, root, base_url):
    """ Convert a plain DOM entry to a pretty blockquote """

    out_html = '<p>'

    author = dom_extract.guess_author(dom, root)
    if author:
        out_html += author + ': '

    url = dom_extract.guess_canonical_url(dom, root, base_url)
    out_html += '<a href="{url}">{title}</a>'.format(
        url=url,
        title=dom_extract.guess_title(dom, root, base_url))

    out_html += '</p>'

    out_html += '<blockquote cite="{url}">{content}</blockquote>'.format(
        url=url,
        content=dom_extract.guess_content(dom))

    return out_html


def _extract(text, url):
    mf_doc = mf2py.parse(text)
    if mf_doc.get('items'):
        LOGGER.info("Found mf2 document")
        return [_extract_mf(item, url) for item in mf_doc['items']]

    # no valid mf2, so let's extract from DOM instead
    dom = BeautifulSoup(text, features='html.parser')
    articles = (dom.find_all('article')
                or dom.find_all(class_='entry')
                or dom.find_all(class_='article')
                or [dom])

    LOGGER.info("Attempting to extract from ad-hoc HTML")

    return [_extract_dom(item, dom, url) for item in articles]


def convert_text(text, base_url, output_format):
    """ Convert an HTML document to output markup; attempts to find
    a plausible article to excerpt.

    Arguments:

    doc -- the BeautifulSoup document object

    base_url -- the base URL of the original document

    format -- the output format to use; uses anything supported by Pandoc

    Returns: the converted document fragment
    """

    out_html = '\n\n'.join(_extract(text, base_url))

    # create a new DOM document from the joined blockquotes
    out_dom = BeautifulSoup(out_html, features='html.parser')

    # convert all href, src, and srcset attributes
    for attr in ('href', 'src'):
        for node in out_dom.findAll(**{attr: True}):
            node[attr] = urllib.parse.urljoin(base_url, node[attr])
    for node in out_dom.findAll(srcset=True):
        node['srcset'] = _rewrite_srcset(node['srcset'], base_url)

    # strip out attributes we don't want
    for attr in ('id', 'class'):
        for node in out_dom.findAll(**{attr: True}):
            del node[attr]

    return pypandoc.convert_text(out_dom.decode_contents(),
                                 output_format, 'html')


def convert(url, output_format):
    """ Given a URL, make an entry file.

    Arguments:

    url -- the URL of the document

    format -- the content format of the document
    """

    req = requests.get(url)
    if not 200 <= req.status_code < 300:
        req.raise_for_status()

    return convert_text(req.text, req.url, output_format)
