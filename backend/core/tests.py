"""Django unit tests for core views."""

from unittest.mock import patch

from django.test import TestCase, RequestFactory

from core.views import get_page_number, get_page_articles


# Tests for the get_page_number function
class GetPageNumberTests(TestCase):

    def test_missing_page_defaults_to_one(self):
        request = RequestFactory().get("/")
        result = get_page_number(request)
        self.assertEqual(result, 1)

    def test_valid_page_number(self):
        request = RequestFactory().get("/?page=3")
        result = get_page_number(request)
        self.assertEqual(result, 3)

    def test_invalid_page_defaults_to_one(self):
        request = RequestFactory().get("/?page=abc")
        result = get_page_number(request)
        self.assertEqual(result, 1)

    def test_zero_page_defaults_to_one(self):
        request = RequestFactory().get("/?page=0")
        result = get_page_number(request)
        self.assertEqual(result, 1)

    def test_negative_page_defaults_to_one(self):
        request = RequestFactory().get("/?page=-2")
        result = get_page_number(request)
        self.assertEqual(result, 1)


# Tests for the get_page_articles function
class GetPageArticlesTests(TestCase):

    # Test that get_page_articles returns articles for the requested page
    @patch("core.views.search_articles")
    def test_returns_articles_for_requested_page(self, mock_search_articles):
        mock_articles = [
            {"title": "Article 1"},
            {"title": "Article 2"},
            {"title": "Article 3"},
        ]
        
        mock_search_articles.return_value = (mock_articles, True)
        request = RequestFactory().get("/?page=2")
        articles, page, has_next, original_page = get_page_articles(
            request,
            "test query"
        )
        
        self.assertEqual(articles, mock_articles)
        self.assertEqual(page, 2)
        self.assertTrue(has_next)
        self.assertEqual(original_page, 2)

    # Test that get_page_articles only returns 12 articles when more than 12 are available
    @patch("core.views.search_articles")
    def test_limits_articles_to_twelve(self, mock_search_articles):
        mock_articles = [{"title": f"Article {i}"} for i in range(15)]
        mock_search_articles.return_value = (mock_articles, True)
        request = RequestFactory().get("/?page=1")
        articles, page, has_next, original_page = get_page_articles(
            request,
            "test query"
        )
        
        self.assertEqual(len(articles), 12)
        self.assertEqual(page, 1)
        self.assertTrue(has_next)
        self.assertEqual(original_page, 1)

    # Test get_category_articles when use_category is True
    @patch("core.views.get_category_articles")
    def test_uses_category_articles_when_requested(self, mock_get_category_articles):
        mock_articles = [
            {"title": "Technology Article 1"},
            {"title": "Technology Article 2"},
        ]
        
        mock_get_category_articles.return_value = (mock_articles, True)
        request = RequestFactory().get("/?page=2")
        articles, page, has_next, original_page = get_page_articles(
            request,
            "technology",
            use_category=True
        )
        
        self.assertEqual(articles, mock_articles)
        self.assertEqual(page, 2)
        self.assertTrue(has_next)
        self.assertEqual(original_page, 2)

    # Test that get_page_articles goes back to the previous page if no articles are found on the requested page
    @patch("core.views.search_articles")
    def test_falls_back_to_previous_page_if_no_articles_are_found(self, mock_search_articles):
        mock_search_articles.side_effect = [
            ([], True),  # Page 3 returns no articles
            ([{"title": "Article 1"}], False),
        ]
        
        request = RequestFactory().get("/?page=3")
        articles, page, has_next, original_page = get_page_articles(
            request,
            "test query"
        )
        
        self.assertEqual(articles, [{"title": "Article 1"}])
        self.assertEqual(page, 2)
        self.assertFalse(has_next)
        self.assertEqual(original_page, 3)

    # Test for the home view
    @patch("core.views.search_articles")
    @patch("core.views.get_category_articles")
    def test_home_view(self, mock_get_category_articles, mock_search_articles):
        trending_articles = [{"title": f"Trending {i}"} for i in range(5)]
        mock_articles = [{"title": f"Article {i}"} for i in range(5)]
        mock_get_category_articles.return_value = (trending_articles, True)
        mock_search_articles.return_value = (mock_articles, True)
        
        response = self.client.get("/")
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertEqual(len(response.context["trending_articles"]), 3)
        self.assertEqual(len(response.context["ai_articles"]), 3)
        self.assertEqual(len(response.context["cybersecurity_articles"]), 3)
        self.assertEqual(len(response.context["gaming_articles"]), 3)
        
    # Test for the AI view
    @patch("core.views.search_articles")
    def test_ai_view(self, mock_search_articles):
        mock_articles = [{"title": f"AI Article {i}"} for i in range(5)]
        mock_search_articles.return_value = (mock_articles, True)

        response = self.client.get("/ai/")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "ai.html")
        self.assertEqual(len(response.context["articles"]), 5)
        
    # Test for the Cybersecurity view
    @patch("core.views.search_articles")
    def test_cybersecurity_view(self, mock_search_articles):
        mock_articles = [{"title": f"Cybersecurity Article {i}"} for i in range(5)]
        mock_search_articles.return_value = (mock_articles, True)

        response = self.client.get("/cybersecurity/")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cybersecurity.html")
        self.assertEqual(len(response.context["articles"]), 5)

    # Test for the Gaming view
    @patch("core.views.search_articles")
    def test_gaming_view(self, mock_search_articles):
        mock_articles = [{"title": f"Gaming Article {i}"} for i in range(5)]
        mock_search_articles.return_value = (mock_articles, True)

        response = self.client.get("/gaming/")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "gaming.html")
        self.assertEqual(len(response.context["articles"]), 5)
        
    # Test for the Trending view
    @patch("core.views.get_category_articles")
    def test_trending_view(self, mock_get_category_articles):
        mock_articles = [{"title": f"Trending Article {i}"} for i in range(5)]
        mock_get_category_articles.return_value = (mock_articles, True)

        response = self.client.get("/trending/")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "trending.html")
        self.assertEqual(len(response.context["articles"]), 5)