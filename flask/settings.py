import os

KEEPER_URL = os.getenv('KEEPER_URL', 'http://keeper:8000')
PROJECTER_URL = os.getenv('PROJECTER_URL', 'http://projecter:8000')
RATER_URL = os.getenv('RATER_URL', 'http://rater:8000')
SEARCHER_URL = os.getenv('SEARCHER_URL', 'http://searcher:8000')
SURVEYER_URL = os.getenv('SURVEYER_URL', 'http://surveyer:8000')