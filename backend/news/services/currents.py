import logging
import os

import requests
from dotenv import load_dotenv

from .cache import TTLCache


logger = logging.getLogger(__name__)

load_dotenv()


# -----------------------------
# API CONFIGURATION
# -----------------------------

BASE_URL = "https://api.currentsapi.services/v1/search"

API_KEY = os.environ.get("CURRENTS_API_KEY")


# -----------------------------
# CACHE
# -----------------------------

_cache = TTLCache(duration_seconds=21600)  # 6 hours


# -----------------------------
# API REQUEST
# -----------------------------

def fetch_articles(params):
    """
    Sends a request to Currents API.

    Uses a simple memory cache to avoid
    unnecessary API calls.
    """

    # Generate a cache key based on the request parameters
    cache_key = str(sorted(params.items()))

    cached = _cache.get(cache_key)
    if cached is not None:
        return cached

    if not API_KEY:

        logger.warning(
            "Currents API key missing."
        )

        return []

    try:

        response = requests.get(
            BASE_URL,
            headers={
                "Authorization": API_KEY
            },
            params=params,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        # Extract articles from the response
        articles = data.get(
            "news",
            []
        )

        _cache.set(cache_key, articles)

        return articles

    except requests.RequestException as error:

        logger.warning(
            f"Currents API error: {error}"
        )

        return []


# -----------------------------
# ARTICLE SEARCH
# -----------------------------

def search_articles(query):

    articles = fetch_articles({

        "keywords": query,
        "language": "en"

    })
    return _deduplicate(articles)


# -----------------------------
# CATEGORY FETCHING
# -----------------------------

def get_category_articles(category):

    articles = fetch_articles({

        "category": category,
        "language": "en"

    })
    return _deduplicate(articles)
    
#-----------------------------
# DEDUPLICATION
#-----------------------------

def _deduplicate(articles):
    seen = set()
    unique = []

    # Prevent duplicates based on the article URL
    for article in articles:
        url = article.get("url")
        if url and url not in seen:
            seen.add(url)
            unique.append(article)

    return unique