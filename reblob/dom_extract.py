""" Methods for extracting stuff from DOM objects """


def get_meta(dom, property):
    """ Get the content from an OpenGraph tag, if present """
    node = dom.find('meta', property=property)
    if node:
        return node.get('content')
    return None


def guess_title(dom, root, base_url):
    """ Attempt to guess an article's title """

    # node with class or id 'title'
    node = dom.find(class_='title') or dom.find(id='title')
    if node:
        return node.decode_contents()

    # guess by common header nestings
    for name in ('h2', 'h3', 'h1'):
        nodes = dom.find_all(name)
        if len(nodes) == 1:
            return nodes[0].decode_contents()

    # OpenGraph tag
    og_title = get_meta(root, 'og:title')
    if og_title:
        return og_title

    # parse the <title> node
    node = root.find('title')
    if node:
        return title_node.decode_contents()

    # just use the URL...
    return base_url


def guess_author(dom, root):
    """ Attempt to guess an article's author name """

    # node with class or 'author'
    node = dom.find(class_='author') or dom.find(id='author')
    if node:
        return node.decode_contents()

    # Meta tag
    meta_name = get_meta(root, 'author') or get_meta(root, 'og:creator')
    if meta_name:
        return meta_name

    return None


def guess_canonical_url(dom, root, base_url):
    """ Attempt to guess an article's base URL """

    # article's own metadata
    node = dom.find('a', rel=['permalink', 'canonical', 'shortcut'])
    if node and 'href' in node:
        return node['href']

    # page metadata
    node = root.find('link', rel=['permalink', 'canonical', 'shortcut'])
    if node and 'href' in node:
        return node['href']

    return base_url


def guess_content(dom):
    """ Attempt to extract the content from an article """
    content = (dom.find(class_='content')
               or dom.find(id='content')
               or dom.find(class_='body')
               or dom)
    return content.decode_contents()
