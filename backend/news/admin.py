from django.contrib import admin
from .models import Article, Bookmark, Comment

admin.site.register(Article)
admin.site.register(Bookmark)
admin.site.register(Comment)


