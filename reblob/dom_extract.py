""" Methods for extracting stuff from DOM objects """

import logging

LOGGER = logging.getLogger('dom')


def get_meta(dom, prop):
    """ Get the content from an OpenGraph tag, if present """
    node = dom.find('meta', property=prop)
    if node:
        content = node.get('content')
        LOGGER.debug("found meta %s = '%s'", prop, content)
        return content
    return None


def guess_title(dom, root, base_url):
    """ Attempt to guess an article's title """

    # OpenGraph tag
    og_title = get_meta(root, 'og:title')
    if og_title:
        LOGGER.debug("using og:title %s", og_title)
        return og_title

    # node with class or id 'title'
    node = dom.find(class_='title') or dom.find(id='title')
    if node:
        LOGGER.debug("title node %s", node)
        return node.decode_contents()

    # guess by common header nestings
    for name in ('h2', 'h3', 'h1'):
        nodes = dom.find_all(name)
        if len(nodes) == 1:
            LOGGER.debug("header node %s", nodes[0])
            return nodes[0].decode_contents()

    # parse the <title> node
    node = root.find('title')
    if node:
        LOGGER.debug("DOM title %s", node)
        return node.decode_contents()

    # just use the URL...
    LOGGER.warning("Couldn't find title for %s; using URL instead", base_url)
    return base_url


def guess_author(dom, root):
    """ Attempt to guess an article's author name """

    # Meta tag
    meta_name = get_meta(root, 'author') or get_meta(root, 'og:creator')
    if meta_name:
        return meta_name

    # node with class or 'author'
    node = dom.find(class_='author') or dom.find(id='author')
    if node:
        LOGGER.debug("Found probable author %s", node)
        return node.decode_contents()

    LOGGER.info("Couldn't find an author name")
    return None


def guess_canonical_url(dom, root, base_url):
    """ Attempt to guess an article's base URL """

    # article's own metadata
    node = dom.find('a', rel=['permalink', 'canonical', 'shortcut'], href=True)
    if node:
        LOGGER.debug("permalink from %s", node)
        return node['href']

    # page metadata
    node = root.find(
        'link', rel=['permalink', 'canonical', 'shortcut'], href=True)
    if node:
        LOGGER.debug("permalink from %s", node)
        return node['href']

    LOGGER.debug("permalink from base_url %s", base_url)
    return base_url


def guess_content(dom):
    """ Attempt to extract the content from an article """
    content = (dom.find(class_='content')
               or dom.find(id='content')
               or dom.find(class_='body')
               or dom)

    LOGGER.debug("content node: %s", content)
    return content.decode_contents()
