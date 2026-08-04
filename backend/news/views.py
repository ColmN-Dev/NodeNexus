from django.shortcuts import render
from django.http import JsonResponse

from .services.currents import get_category_articles, search_articles

def home(request):
    """
    Featured articles view.
    Displays curated technology articles for the homepage.
    """
    # Trending Technology
    trending_articles = get_category_articles("technology")[:3]


    # Artificial Intelligence
    ai_articles = search_articles(
        "'artificial intelligence' OR 'machine learning' OR 'OpenAI' OR 'ChatGPT' OR 'generative AI' OR 'Claude' OR 'Anthropic'"
    )[:3]


    # Cybersecurity
    cybersecurity_articles = search_articles(
        "'cybersecurity' OR ransomware OR malware OR 'cyber attacks'"
    )[:3]


    # Gaming
    gaming_articles = search_articles(
        "videogames OR PlayStation OR Xbox OR Nintendo OR 'PC gaming'"
    )[:3]


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
    
    # Limit to 12 results
    articles = search_articles(query)[:12] if query else [] 
    

    context = {
        "query": query,
        "articles": articles,
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

    # Limit to 8 results and return only titles
    articles = search_articles(query)[:8]
    titles = [article.get("title") for article in articles if article.get("title")]

    return JsonResponse(titles, safe=False)