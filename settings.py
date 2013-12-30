AUTHOR = "Mathieu Leplatre"
SITEURL = "http://blog.mathieu-leplatre.info"
SITENAME = "Mathieu Leplatre"
LOCALE = 'en_US.utf8'
TIMEZONE = 'Europe/Paris'

DISPLAY_PAGES_ON_MENU = True
WITH_PAGINATION = True
DEFAULT_PAGINATION = 7
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'
RELATIVE_URLS = False
DELETE_OUTPUT_DIRECTORY = True

TWITTER_USERNAME = "leplatrem"
GITHUB_URL = "https://github.com/leplatrem"
DISQUS_SITENAME = "mathieuleplatre"
PIWIK_URL = "mathieu-leplatre.info/piwik"
PIWIK_SITE_ID = 1

SOCIAL = (
    ("LinkedIn", "http://www.linkedin.com/in/leplatre"),
    ("Launchpad", "https://code.launchpad.net/~mathieu.leplatre"),
    ("GitHub", "https://github.com/leplatrem"),
    ("Google+", "https://plus.google.com/u/0/106965745149150173373"),
    ("Twitter", "http://twitter.com/leplatrem"),
    ("Identi.ca", "http://identi.ca/leplatrem"),
)

STATIC_PATHS = ['images', 'extra/CNAME']
EXTRA_PATH_METADATA = {'extra/CNAME': {'path': 'CNAME'},}
