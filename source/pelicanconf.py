#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
import os

AUTHOR = 'Bogdan Ivanyuk'
SITENAME = 'Bogdan Ivanyuk-Skulskyi'
SITEURL = os.environ.get('SITEURL', '')
SITESUBTITLE = 'Senior ML Engineer & Kaggle Expert'

PATH = 'content'
OUTPUT_PATH = '../'
DELETE_OUTPUT_DIRECTORY = False

TIMEZONE = 'Europe/Paris'
DEFAULT_LANG = 'en'
DEFAULT_DATE_FORMAT = '%Y-%m-%d'

# Markdown extensions
MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {'css_class': 'highlight'},
        'markdown.extensions.extra': {},
        'markdown.extensions.meta': {},
        'markdown.extensions.toc': {},
    }
}

# Feed generation
FEED_ALL_ATOM = None
FEED_ALL_RSS = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

PLUGINS = []
THEME = 'theme'

# Navigation
DISPLAY_PAGES_ON_MENU = False
DISPLAY_CATEGORIES_ON_MENU = False

# Article settings
ARTICLE_PATHS = ['articles']
ARTICLE_SAVE_AS = '{slug}/index.html'
ARTICLE_URL = '{slug}/'

# Page settings
PAGE_PATHS = ['pages']
PAGE_SAVE_AS = '{slug}/index.html'
PAGE_URL = '{slug}/'

# URLs
INDEX_SAVE_AS = ''
ARCHIVES_SAVE_AS = ''

# Fix deprecated settings
PAGINATED_TEMPLATES = {}

# Static files
STATIC_PATHS = ['static']
EXTRA_PATH_METADATA = {
    'static/.htaccess': {'path': '.htaccess'},
}

# Author and social
AUTHOR_EMAIL = 'ivanyuk.bogdan1999@gmail.com'
SOCIAL = (
    ('Email', 'mailto:ivanyuk.bogdan1999@gmail.com'),
    ('Twitter', 'https://twitter.com/bogdan_ivanyuk'),
    ('GitHub', 'https://github.com/KyloRen1'),
    ('LinkedIn', 'https://www.linkedin.com/in/bogdan-ivanyuk-skulskiy-982739163/'),
    ('Kaggle', 'https://www.kaggle.com/bogdanbaraban'),
)

# Default Pelican settings
DEFAULT_PAGINATION = 10
PAGINATED_DIRECT_TEMPLATES = []

# Output
OUTPUT_RETENTION = ['.git', '.gitignore', 'CNAME']

AUTHOR_SAVE_AS = False
CATEGORY_SAVE_AS = False
TAG_SAVE_AS = False
