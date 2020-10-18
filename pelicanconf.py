#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = 'Mathieu Leplatre'
SITENAME = 'Mathieu Leplatre'
SITEURL = 'https://blog.mathieu-leplatre.info'

PATH = 'content'

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = []

# Social widget
SOCIAL = (
    ("LinkedIn", "https://www.linkedin.com/in/leplatre"),
    ("Launchpad", "https://code.launchpad.net/~mathieu.leplatre"),
    ("GitHub", "https://github.com/leplatrem"),
    ("Twitter", "https://twitter.com/leplatrem"),
)

DISQUS_SITENAME = "mathieuleplatre"

STATIC_PATHS = ['images', 'extra/CNAME']
EXTRA_PATH_METADATA = {'extra/CNAME': {'path': 'CNAME'},}

DEFAULT_PAGINATION = 10

RELATIVE_URLS = True

THEME = 'themes/mnmlist'
