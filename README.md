# reblob

Tool for doing a reblog/reply/whatever of an existing webpage.

Given a URL, it will produce a response blog entry with the original content wrapped in a block quote, before using [Pandoc](https://pandoc.org) to convert it to the representation of choice.

Usage:

```bash
pip install reblob
reblob http://example.com/ -f rst
```

It requires Pandoc to be installed; see the [pypandoc](https://github.com/bebraw/pypandoc) manual for some suggestions on how to do this.
