from django.db import models
from django.contrib.auth.models import User

# Article model to store news articles with fields for title,
# description, image URL, publication date, source, and URL.
# The URL field is unique to prevent duplicate articles.
# The created_at field automatically records when the article was added to the database.
class Article(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    image = models.URLField(max_length=1000, blank=True)
    published = models.DateTimeField(null=True, blank=True)
    source = models.TextField(blank=True)
    url = models.URLField(max_length=1000, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # String representation of the Article model,
    # returning the title of the article.
    def __str__(self):
        return self.title
    
# Bookmark model to allow users to bookmark articles.
class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    # Ensure that a user can only bookmark a specific article once by enforcing a unique constraint on the combination of user and article fields.
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "article"],
                name="unique_user_article_bookmark"
            )
        ]

    # String representation of the Bookmark model,
    # returning a string that includes the username of the user and the title of the article they bookmarked.
    def __str__(self):
        return f"{self.user.username} - {self.article.title}"