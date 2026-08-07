#core/views.py

from django.shortcuts import render
from django.http import HttpResponseRedirect
from news.services.currents import search_articles, get_category_articles


"""
Helper function to get articles for a specific page, handling cases where the requested page has no articles
"""

def get_page_articles(request, query, use_category=False):
    page = int(request.GET.get("page", 1))
    original_page = page

    # Get articles based on whether to use category or search
    if use_category:
        articles, has_next = get_category_articles(query, page=page)
    else:
        articles, has_next = search_articles(query, page=page)

    # If the requested page has no articles, go back one page until articles are found or redirect to the first page
    while page > 1 and not articles:
        page -= 1

        if use_category:
            articles, has_next = get_category_articles(query, page=page)
        else:
            articles, has_next = search_articles(query, page=page)

    return articles[:12], page, has_next, original_page


"""
Core views for the NodeNexus application.

"""
def ai(request):
    
    query = "'artificial intelligence' OR 'machine learning' OR 'OpenAI' OR 'ChatGPT' OR 'generative AI' OR 'Claude' OR 'Anthropic'"
    
    articles, page, has_next, original_page = get_page_articles(
        request, query
    )

    if page != original_page:
        return HttpResponseRedirect(f"?page={page}")

    return render(
        request,
        "ai.html",
        {"articles": articles, "page": page, "has_next": has_next}
    )

def cybersecurity(request):
    
    query = "'cybersecurity' OR ransomware OR malware OR 'cyber attacks'"
    
    articles, page, has_next, original_page = get_page_articles(
        request, query
    )

    if page != original_page:
        return HttpResponseRedirect(f"?page={page}")

    return render(
        request,
        "cybersecurity.html",
        {"articles": articles, "page": page, "has_next": has_next}
    )

def gaming(request):
    
    query = "videogames OR PlayStation OR Xbox OR Nintendo OR 'PC gaming'"
    
    articles, page, has_next, original_page = get_page_articles(
        request, query
    )

    if page != original_page:
        return HttpResponseRedirect(f"?page={page}")

    return render(
        request,
        "gaming.html",
        {"articles": articles, "page": page, "has_next": has_next}
    )

def trending(request):
    
    
    articles, page, has_next, original_page = get_page_articles(
        request, "technology", use_category=True
    )

    if page != original_page:
        return HttpResponseRedirect(f"?page={page}")

    return render(
        request,
        "trending.html",
        {"articles": articles, "page": page, "has_next": has_next}
    )