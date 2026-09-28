"""Django tests for the news views."""

from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth.models import User
import cloudinary
from news.views import search_results
from news.models import Article, Bookmark, Comment
from datetime import datetime, timedelta
from django.utils import timezone


class SearchResultsTests(TestCase):
    """Tests for the search_results view."""

    @patch("news.views.search_articles")
    def test_search_results(self, mock_search_articles):
        mock_articles = [{"title": f"Article {i}"} for i in range(15)]
        mock_search_articles.return_value = (mock_articles, True)
        
        response = self.client.get("/search/?q=test")
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "search_results.html")
        self.assertEqual(response.context["query"], "test")
        self.assertEqual(len(response.context["articles"]), 12)

class AutoCompleteTests(TestCase):
    """Tests for the auto_complete view."""

    @patch("news.views.search_articles")
    def test_auto_complete_returns_titles(self, mock_search_articles):
        mock_articles = [{"title": f"Article {i}"} for i in range(10)]
        mock_search_articles.return_value = (mock_articles, True)

        response = self.client.get("/auto-complete/?q=test")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 8)
        self.assertEqual(response.json()[0], "Article 0")
        
    def test_auto_complete_returns_empty_query(self):

        response = self.client.get("/auto-complete/?q=")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])
        
        
class ArticleDetailTests(TestCase):
    """Tests for the article_detail view."""

    @patch("news.views.search_articles")
    def test_article_detail(self, mock_search_articles):
        mock_search_articles.return_value = ([], False)

        response = self.client.get("/article/?title=Test+Article&description=Test+description&image=test.jpg&published=2026-09-30&source=Test+Source&url=https://example.com")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "article_detail.html")
        self.assertEqual(response.context["article"]["title"], "Test Article")
        self.assertEqual(response.context["article"]["description"], "Test description")
        self.assertEqual(response.context["article"]["image"], "test.jpg")
        self.assertEqual(response.context["article"]["published"], "2026-09-30")
        self.assertEqual(response.context["article"]["source"], "Test Source")
        self.assertEqual(response.context["article"]["url"], "https://example.com")
    
    def test_article_detail_missing_url(self):

        response = self.client.get("/article/?title=Test+Article")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "article_detail.html")
        self.assertEqual(response.context["error"], "Article URL is missing.")
        
    @patch("news.views.search_articles")
    def test_article_detail_with_saved_article(self, mock_search_articles):
        article = Article.objects.create(
            title="Saved Article",
            description="Saved description",
            image="saved.jpg",
            published=timezone.make_aware(datetime(2026, 9, 30)),
            source="Saved Source",
            url="https://example.com/saved",
        )
        mock_search_articles.return_value = ([], False)
        
        response = self.client.get(f"/article/{article.id}/")
        
        self.assertEqual(response.context["article"]["title"], "Saved Article")
        self.assertEqual(response.context["article"]["description"], "Saved description")
        self.assertEqual(response.context["article"]["image"], "saved.jpg")
        self.assertEqual(response.context["article"]["published"].date().isoformat(), "2026-09-30")
        self.assertEqual(response.context["article"]["source"], "Saved Source")
        self.assertEqual(response.context["article"]["url"], "https://example.com/saved")
        
    @patch("news.views.search_articles")
    def test_article_detail_bookmarked_article(self, mock_search_articles):
        mock_search_articles.return_value = ([], False)
        
        user = User.objects.create_user(username="testuser", password="testpassword123")
        
        cloudinary.config(cloud_name="test-cloud")
        
        self.client.login(username="testuser", password="testpassword123")
        
        article = Article.objects.create(
            title="Bookmarked Article",
            description="Bookmarked description",
            image="https://example.com/image.jpg",
            published=timezone.make_aware(datetime(2026, 9, 30)),
            source="Bookmarked Source",
            url="https://example.com/bookmarked",
        )
        
        bookmark = Bookmark.objects.create(user=user, article=article)
        
        response = self.client.get(f"/article/{article.id}/")
        
        self.assertTrue(response.context["is_bookmarked"])
        self.assertEqual(response.context["bookmark"], bookmark)
    
    @patch("news.views.get_or_create_article")
    def test_bookmark_article(self, mock_get_or_create_article):
        
        user = User.objects.create_user(username="testuser", password="testpassword123")
        
        self.client.login(username="testuser", password="testpassword123")

        article = Article.objects.create(
            title="Test Article",
            description="Test description",
            url="https://example.com/test-article",
        )
        
        mock_get_or_create_article.return_value = (article, True)
        
        response = self.client.post("/article/bookmark/", {
            "title": article.title,
            "description": article.description,
            "image": article.image,
            "source": article.source,
            "url": article.url,
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Bookmark.objects.filter(user=user, article=article).exists())
        
    def test_delete_bookmark(self):
        
        user = User.objects.create_user(username="testuser", password="testpassword123")
        
        self.client.login(username="testuser", password="testpassword123")

        article = Article.objects.create(
            title="Test Article",
            description="Test description",
            url="https://example.com/test-article",
        )
        
        Bookmark.objects.create(user=user, article=article)
        
        response = self.client.post(f"/article/{article.id}/delete/")
        
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Bookmark.objects.filter(user=user, article=article).exists())
        self.assertFalse(Article.objects.filter(id=article.id).exists())
        
    @patch("news.views.get_or_create_article")
    def test_add_comment(self, mock_get_or_create_article):
        
        user = User.objects.create_user(username="testuser", password="testpassword123")
        
        self.client.login(username="testuser", password="testpassword123")
        
        article = Article.objects.create(
            title="Test Article",
            description="Test description",
            url="https://example.com/test-article",
        )
        
        mock_get_or_create_article.return_value = (article, True)
        
        response = self.client.post(f"/article/comment/", {
            "title": article.title,
            "description": article.description,
            "image": article.image,
            "source": article.source,
            "url": article.url,
            "content": "This is a test comment.",
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Comment.objects.filter(user=user, article=article, content="This is a test comment.").exists())
        
    @patch("news.views.get_or_create_article")
    def test_add_reply(self, mock_get_or_create_article):
        
        user = User.objects.create_user(username="testuser", password="testpassword123")
        
        self.client.login(username="testuser", password="testpassword123")
        
        article = Article.objects.create(
            title="Test Article",
            description="Test description",
            url="https://example.com/test-article",
        )
        
        parent_comment = Comment.objects.create(user=user, article=article, content="This is the original comment.")
        
        mock_get_or_create_article.return_value = (article, True)
        
        response = self.client.post(f"/article/comment/", {
            "title": article.title,
            "description": article.description,
            "image": article.image,
            "source": article.source,
            "url": article.url,
            "content": "This is a reply.",
            "parent_id": parent_comment.id,
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Comment.objects.filter(user=user, article=article, content="This is a reply.", parent=parent_comment).exists())
        
    def test_edit_comment(self):
        
        user = User.objects.create_user(username="testuser", password="testpassword123")
        
        self.client.login(username="testuser", password="testpassword123")
        
        article = Article.objects.create(
            title="Test Article",
            description="Test description",
            url="https://example.com/test-article",
        )
        
        comment = Comment.objects.create(user=user, article=article, content="This is the original comment.")
        
        response = self.client.post(f"/article/comment/{comment.id}/edit/", {
            "content": "This is the edited comment.",
        })
        
        comment.refresh_from_db()
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(comment.content, "This is the edited comment.")
        self.assertTrue(comment.is_edited)
        
    def test_edit_comment_after_15_minutes(self):
        
        user = User.objects.create_user(username="testuser", password="testpassword123")
        
        self.client.login(username="testuser", password="testpassword123")
        
        article = Article.objects.create(
            title="Test Article",
            description="Test description",
            url="https://example.com/test-article",
        )
        
        comment = Comment.objects.create(user=user, article=article, content="This is the original comment.")
        
        comment.created_at = timezone.now() - timedelta(minutes=16)
        comment.save()
        
        response = self.client.post(f"/article/comment/{comment.id}/edit/", {
            "content": "This is the edited comment.",
        })
        
        comment.refresh_from_db()
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(comment.content, "This is the original comment.")
        self.assertFalse(comment.is_edited)

    def test_delete_comment(self):
        
        user = User.objects.create_user(username="testuser", password="testpassword123")
        
        self.client.login(username="testuser", password="testpassword123")
        
        article = Article.objects.create(
            title="Test Article",
            description="Test description",
            url="https://example.com/test-article",
        )
        
        comment = Comment.objects.create(user=user, article=article, content="Test comment.")
        
        response = self.client.post(f"/article/comment/{comment.id}/delete/")
        
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Comment.objects.filter(id=comment.id).exists())
        self.assertFalse(Article.objects.filter(id=article.id).exists())
        
    def test_delete_comment_not_owner(self):
        
        user1 = User.objects.create_user(username="user1", password="password123")
        user2 = User.objects.create_user(username="user2", password="password456")
        
        self.client.login(username="user2", password="password456")
        
        article = Article.objects.create(
            title="Test Article",
            description="Test description",
            url="https://example.com/test-article",
        )
        
        comment = Comment.objects.create(user=user1, article=article, content="Test comment.")
        
        response = self.client.post(f"/article/comment/{comment.id}/delete/")
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Comment.objects.filter(id=comment.id).exists())