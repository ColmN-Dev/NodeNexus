#news/urls.py

from django.urls import path
from . import views

urlpatterns = [
    
    path('search/', views.search_results, name='search_results'),
    
    path('auto-complete/', views.auto_complete, name='auto_complete'),
    
    path('article/', views.article_detail, name='article_detail'),
    
    path('article/<int:article_id>/', views.article_detail, name='saved_article_detail'),
    
    path('article/comment/', views.add_comment, name='add_comment'),
    
    path('article/comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    
    path('article/<int:article_id>/delete/', views.delete_bookmark, name='delete_bookmark'),
    
    path('article/comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    
    path('article/bookmark/', views.bookmark_article, name='bookmark_article'),
    
]