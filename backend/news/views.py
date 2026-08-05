from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect

from .services.currents import get_category_articles, search_articles

def home(request):
    """
    Featured articles view.
    Displays curated technology articles for the homepage.
    """
    # Trending Technology
    trending_articles, _ = get_category_articles("technology", page=1)
    
    trending_articles = trending_articles[:3]


    # Artificial Intelligence
    ai_articles, _ = search_articles(
        "'artificial intelligence' OR 'machine learning' OR 'OpenAI' OR 'ChatGPT' OR 'generative AI' OR 'Claude' OR 'Anthropic'"
    )
    
    ai_articles = ai_articles[:3]


    # Cybersecurity
    cybersecurity_articles, _ = search_articles(
        "'cybersecurity' OR ransomware OR malware OR 'cyber attacks'"
    )
    
    cybersecurity_articles = cybersecurity_articles[:3]


    # Gaming
    gaming_articles, _ = search_articles(
        "videogames OR PlayStation OR Xbox OR Nintendo OR 'PC gaming'"
    )
    
    gaming_articles = gaming_articles[:3]


    context = {
        "trending_articles": trending_articles,
        "ai_articles": ai_articles,
        "cybersecurity_articles": cybersecurity_articles,
        "gaming_articles": gaming_articles,
    }

    return render(
        request,
        "index.html",
        context
    )
    
def search_results(request):
    """
    Search results view.
    Displays articles based on user search queries.
    """

    query = request.GET.get("q", "").strip()

    page = int(request.GET.get("page", 1))

    if query:
        articles, has_next = search_articles(query, page=page)
    else:
        articles = []
        has_next = False

    original_page = page

    while page > 1 and not articles:
        page -= 1

        articles, has_next = search_articles(
            query,
            page=page
        )

    if page != original_page:
        return HttpResponseRedirect(f"?q={query}&page={page}")

    articles = articles[:12]

    context = {
        "query": query,
        "articles": articles,
        "page": page,
        "has_next": has_next,
    }

    return render(
        request,
        "search_results.html",
        context
    )
    
def auto_complete(request):
    """
    Autocomplete view.
    Returns matching article titles as JSON for the search dropdown.
    """
    query = request.GET.get("q", "").strip()

    # Return an empty list if the query is empty
    if not query:
        return JsonResponse([], safe=False)
    
    # Get articles from API response
    articles, _ = search_articles(query)

    # Limit to 8 results and return only titles
    articles = articles[:8]
    titles = [article.get("title") for article in articles if article.get("title")]

    return JsonResponse(titles, safe=False)