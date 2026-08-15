from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .services.currents import search_articles
from .services.articles import get_or_create_article
from .models import Article, Bookmark


def search_results(request):
    """
    Search results view.
    Displays articles based on user search queries.
    """

    query = request.GET.get("q", "").strip()
    page = int(request.GET.get("page", 1))

    articles = []
    has_next = False

    if query:
        articles, has_next = search_articles(query, page=page)

    original_page = page

    while page > 1 and not articles:
        page -= 1
        articles, has_next = search_articles(query, page=page)

    if page != original_page:
        return HttpResponseRedirect(f"?q={query}&page={page}")

    articles = articles[:12]

    context = {
        "query": query,
        "articles": articles,
        "page": page,
        "has_next": has_next,
    }

    return render(request, "search_results.html", context)


def auto_complete(request):
    """
    Autocomplete view.
    Returns matching article titles as JSON for the search dropdown.
    """

    query = request.GET.get("q", "").strip()

    # Return an empty list if the query is empty
    if not query:
        return JsonResponse([], safe=False)

    # Get articles from the API
    articles, _ = search_articles(query)

    # Limit autocomplete results to 8 titles
    articles = articles[:8]
    titles = [article.get("title") for article in articles if article.get("title")]

    return JsonResponse(titles, safe=False)


def article_detail(request, article_id=None):
    """
    Article detail view.
    Displays detailed information about an article.
    """

    # Load the article from the database if an article_id is provided
    if article_id:
        saved_article = Article.objects.get(id=article_id)
        
        article = {
            "title": saved_article.title,
            "description": saved_article.description,
            "image": saved_article.image,
            "published": saved_article.published,
            "source": saved_article.source,
            "url": saved_article.url,
        }
        
    else:
        # Get the article data from the URL query parameters
        article = {
            "title": request.GET.get("title"),
            "description": request.GET.get("description"),
            "image": request.GET.get("image"),
            "published": request.GET.get("published"),
            "source": request.GET.get("source"),
            "url": request.GET.get("url"),
        }

    # Make sure an article URL was provided
    if not article["url"]:
        return render(request, "article_detail.html", {"error": "Article URL is missing."})

    # Check if the request is from a Meta crawler
    # to avoid unnecessary API calls
    user_agent = request.META.get("HTTP_USER_AGENT", "").lower()
    is_meta_crawler = "meta-externalagent" in user_agent

    related_articles = []

    if not is_meta_crawler:
        # Use the first three words of the title to find related articles
        title_words = article["title"].split()
        related_query = " ".join(title_words[:3])

        related_articles, _ = search_articles(related_query)

        # Remove the current article and limit results to 12 articles
        related_articles = [
            item for item in related_articles
            if item.get("url") != article["url"]
        ][:12]

    context = {
        "article": article,
        "related_articles": related_articles,
    }

    return render(request, "article_detail.html", context)


@login_required
def bookmark_article(request):
    """
    Bookmark article view.
    Allows logged-in users to bookmark articles.
    """

    # Only allow POST requests for bookmarking
    if request.method != "POST":
        return redirect("home")

    # Get the article data submitted by the bookmark form
    article_data = {
        "title": request.POST.get("title"),
        "description": request.POST.get("description"),
        "image": request.POST.get("image"),
        "published": request.POST.get("published"),
        "source": request.POST.get("source"),
        "url": request.POST.get("url"),
    }

    # Create the Article database record only when the user bookmarks it
    article, created = get_or_create_article(article_data)

    # Create the bookmark linking the article to the logged-in user
    bookmark, bookmark_created = Bookmark.objects.get_or_create(
        user=request.user,
        article=article
    )

    messages.success(request, "Article has been bookmarked successfully!")

    return redirect("profile")

@login_required
def delete_bookmark(request, article_id):
    """
    Deletes a user's bookmark and removes the article
    if it is no longer bookmarked by anyone.
    """

    if request.method != "POST":
        return redirect("profile")

    bookmark = Bookmark.objects.filter(
        user=request.user,
        article_id=article_id
    ).first()

    if bookmark:
        article = bookmark.article
        bookmark.delete()

        # Delete the article if nobody else has bookmarked it
        if not Bookmark.objects.filter(article=article).exists():
            article.delete()

        messages.success(request, "Article removed from your bookmarks.")

    return redirect("profile")