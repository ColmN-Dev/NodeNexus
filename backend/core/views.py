#core/views.py

from django.shortcuts import render

from news.services.currents import search_articles, get_category_articles


"""
Core views for the NodeNexus application.
"""
def ai(request):
    
    articles = search_articles(
        "'artificial intelligence' OR 'machine learning' OR 'OpenAI' OR 'ChatGPT' OR 'generative AI' OR 'Claude' OR 'Anthropic'"
    )[:12]  # Limit to 12 results
    
    return render(request, 'ai.html', {'articles': articles})

def cybersecurity(request):
    articles = search_articles(
        "'cybersecurity' OR ransomware OR malware OR 'cyber attacks'"
    )[:12]  # Limit to 12 results

    return render(request, 'cybersecurity.html', {'articles': articles})

def gaming(request):
    articles = search_articles(
        "videogames OR PlayStation OR Xbox OR Nintendo OR 'PC gaming'"
    )[:12]  # Limit to 12 results

    return render(request, 'gaming.html', {'articles': articles})

def trending(request):
    articles = get_category_articles("technology")[:12]  # Limit to 12 results

    return render(request, 'trending.html', {'articles': articles})