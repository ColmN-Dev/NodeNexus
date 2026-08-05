#core/views.py

from django.shortcuts import render
from django.http import HttpResponseRedirect
from news.services.currents import search_articles, get_category_articles


"""
Core views for the NodeNexus application.
"""
def ai(request):
    
    page = int(request.GET.get("page", 1))
        
    articles, has_next = search_articles(
        "'artificial intelligence' OR 'machine learning' OR 'OpenAI' OR 'ChatGPT' OR 'generative AI' OR 'Claude' OR 'Anthropic'",
        page=page
    )
       
    # Store the original page number for redirect    
    original_page = page  
    
    # If someone requests an invalid page, go back one page
    while page > 1 and not articles:
        page -= 1
        
    articles, has_next = search_articles(
    "'artificial intelligence' OR 'machine learning' OR 'OpenAI' OR 'ChatGPT' OR 'generative AI' OR 'Claude' OR 'Anthropic'",
    page=page
    )
                
    if page != original_page:
    # If the user requests a page with no articles, redirect to the previous page
        return HttpResponseRedirect(f"?page={page}")
    
    articles = articles[:12]
        
    return render(request, 'ai.html', {'articles': articles, 'page': page, 'has_next': has_next})

def cybersecurity(request):
    
    page = int(request.GET.get("page", 1))
    
    articles, has_next = search_articles(
        "'cybersecurity' OR ransomware OR malware OR 'cyber attacks'",
        page=page
    )
    
    original_page = page  # Store the original page number for redirect
    
    while page > 1 and not articles:
        page -= 1
        
        articles, has_next = search_articles(
            "'cybersecurity' OR ransomware OR malware OR 'cyber attacks'",
            page=page
        )
        
    if page != original_page:
        # If the user requests a page with no articles, redirect to the previous page
        return HttpResponseRedirect(f"?page={page}")
    
    articles = articles[:12]  
    
    return render(request, 'cybersecurity.html', {'articles': articles, 'page': page, 'has_next': has_next})

def gaming(request):
    
    page = int(request.GET.get("page", 1))
    
    articles, has_next = search_articles(
        "videogames OR PlayStation OR Xbox OR Nintendo OR 'PC gaming'",
        page=page
    )
    
    original_page = page  # Store the original page number for redirect
    
    while page > 1 and not articles:
        page -= 1
        
        articles, has_next = search_articles(
            "videogames OR PlayStation OR Xbox OR Nintendo OR 'PC gaming'",
            page=page
        )
        
    if page != original_page:
        # If the user requests a page with no articles, redirect to the previous page
        return HttpResponseRedirect(f"?page={page}")
    
    articles = articles[:12]
        
    return render(request, 'gaming.html', {'articles': articles, 'page': page, 'has_next': has_next})

def trending(request):
    
    page = int(request.GET.get("page", 1))
    
    articles, has_next = get_category_articles("technology", page=page)
    
    original_page = page  # Store the original page number for redirect
    
    while page > 1 and not articles:
        page -= 1
        
        articles, has_next = get_category_articles("technology", page=page)
        
    if page != original_page:
        # If the user requests a page with no articles, redirect to the previous page
        return HttpResponseRedirect(f"?page={page}")
    
    articles = articles[:12]
        
    return render(request, 'trending.html', {'articles': articles, 'page': page, 'has_next': has_next})