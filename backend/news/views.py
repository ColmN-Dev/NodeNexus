from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from django.utils import timezone
from datetime import timedelta

from .services.currents import search_articles
from .services.articles import get_or_create_article
from .models import Article, Bookmark, Comment


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
    
    comments = []

    # Load the article from the database if an article_id is provided and fetch its comments if available
    if article_id:
        saved_article = Article.objects.get(id=article_id)
        comments = Comment.objects.filter(article=saved_article, parent__isnull=True)
        
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
    
    # Check if the current user has bookmarked this article
    bookmark = None
    
    # Query the database for an existing bookmark
    if request.user.is_authenticated:
        bookmark = Bookmark.objects.filter(user=request.user, article__url=article["url"]).first()

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
        "bookmark": bookmark,
        "is_bookmarked": bookmark is not None,
        "comments": comments,
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
    bookmark, bookmark_created = Bookmark.objects.get_or_create(user=request.user, article=article)

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

    bookmark = Bookmark.objects.filter(user=request.user, article_id=article_id).first()

    if bookmark:
        article = bookmark.article
        bookmark.delete()

        # Delete the article if nobody else has bookmarked it
        if not Bookmark.objects.filter(article=article).exists():
            article.delete()

        messages.success(request, "Article removed from your bookmarks.")

    return redirect("profile")

@login_required
def add_comment(request):
    """
    Adds a comment to an article.
    """
    
    if request.method != "POST":
        return redirect("article_detail")
    
    
    article_data = {
        "title": request.POST.get("title"),
        "description": request.POST.get("description"),
        "image": request.POST.get("image"),
        "published": request.POST.get("published"),
        "source": request.POST.get("source"),
        "url": request.POST.get("url"),
    }
    
    # Create the Article database record only when the user comments on it
    article, created = get_or_create_article(article_data)
    
    content = request.POST.get("content")
    
    # Handle parent comment for nested comments/replies
    parent_id = request.POST.get("parent_id")
    parent_comment = None
    if parent_id:
        parent_comment = Comment.objects.filter(id=parent_id).first()
        
    comment = Comment.objects.create(user=request.user, article=article, content=content, parent=parent_comment)
    
    messages.success(request, "Your comment has been added successfully!")
    
    return redirect("saved_article_detail", article_id=article.id)

@login_required
def edit_comment(request, comment_id):
    """
    Allows a user to edit their comment.
    """
    
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    
    if comment.user != request.user:
        messages.error(request, "You cannot edit this comment.")
        return redirect("saved_article_detail", article_id=comment.article.id)
    
    # Allow editing only within 15 minutes of posting
    edit_window = timedelta(minutes=15)
    if timezone.now() > comment.created_at + edit_window:
        messages.error(request, "Comments can only be edited within 15 minutes of posting.")
        return redirect("saved_article_detail", article_id=comment.article.id)
    
    if request.method == "POST":
        content = request.POST.get("content")
        
        if content == comment.content:
            messages.warning(request, "No changes were made to your comment.")
            return redirect("saved_article_detail", article_id=comment.article.id)
        
        if content:
            comment.content = content
            comment.is_edited = True
            comment.save()
            messages.success(request, "Your comment has been updated successfully!")
        return redirect("saved_article_detail", article_id=comment.article.id)
    
@login_required
def delete_comment(request, comment_id):
    """
    Deletes a user's comment.
    """

    comment = get_object_or_404(Comment, id=comment_id)

    if comment.user != request.user:
        messages.error(request, "You cannot delete this comment.")
        return redirect("saved_article_detail", article_id=comment.article.id)

    article_id = comment.article.id
    comment.delete()

    messages.success(request, "Your comment has been deleted successfully!")

    return redirect("saved_article_detail", article_id=article_id)
