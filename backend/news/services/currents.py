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

# A simple in-memory cache with a time-to-live (TTL) of 6 hours
_cache = TTLCache(duration_seconds=21600)

#-----------------------------
# EXCLUDED DOMAINS
#-----------------------------

# Domains that mostly return auto-generated vulnerability dumps,
# forum threads, or other low-value content rather than genuine articles
EXCLUDED_DOMAINS = [
    "reddit.com",
    "vulners.com",
    "opencve.io",
    "vuldb.com",
    "cve.org",
    "nvd.nist.gov",
    "cisa.gov",
]

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
    # to ensure that identical requests return cached results
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

        # Log the error and return an empty list to avoid crashing the application
        logger.warning(
            f"Currents API error: {error}"
        )

        return []
    

# -----------------------------
# ARTICLE SEARCH
# -----------------------------

def search_articles(query):
    """
    Searches Currents API by free-text keywords,
    then removes duplicates and low-quality results.
    """
    
    articles = fetch_articles({

        "keywords": query,
        "language": "en"
    })
    
    return (_filter_low_quality(_deduplicate(articles)))


# -----------------------------
# CATEGORY FETCHING
# -----------------------------

def get_category_articles(category):
    """
    Fetches articles for a fixed Currents API category,
    then removes duplicates and low-quality results.
    """
    
    articles = fetch_articles({

        "category": category,
        "language": "en"

    })
    return (_filter_low_quality(_deduplicate(articles)))
    
#-----------------------------
# DEDUPLICATION
#-----------------------------

def _deduplicate(articles):
    
    """
    Removes duplicate articles based on their URL.
    """
    
    seen = set()
    unique = []

    # Prevent duplicates based on the article URL
    for article in articles:
        url = article.get("url")
        
        if url and url not in seen:
            seen.add(url)
            unique.append(article)

    return unique

#-----------------------------
# LOW-QUALITY FILTERING
#-----------------------------

def _filter_low_quality(articles):
    """
    Removes articles from excluded domains, and articles that have a CVE in the title and the
    title starts with a raw CVE ID
    """
    
    filtered = []

    for a in articles:
        url = a.get("url", "")
        title = a.get("title", "")

        is_excluded_domain = any(domain in url for domain in EXCLUDED_DOMAINS)
        is_raw_cve_title = title.strip().upper().startswith("CVE")
        
        if is_excluded_domain:
            continue
        
        # Skip articles that have a CVE in the title and start with "CVE"
        # otherwise, keep the article
        if is_raw_cve_title:
            continue  

        filtered.append(a)
        
    return filtered