from ..models import Article

def get_or_create_article(article_data):
    """
    Retrieves an existing Article object based on the provided URL or creates a new one if it doesn't exist.
    The function uses the get_or_create method to either fetch the existing article or create a new one with the provided data.
    """    
    
    article, created = Article.objects.get_or_create(
        url=article_data.get("url"),
        defaults={
            "title": article_data.get("title", ""),
            "description": article_data.get("description", ""),
            "image": article_data.get("image", ""),
            "published": article_data.get("published"),
            "source": article_data.get("source", ""),
        },
    )
    
    return article, created