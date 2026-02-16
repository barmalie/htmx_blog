import pytest
from articles.models import Article
from ..factories import ArticleFactory, UserFactory

@pytest.mark.django_db
class TestArticleModel:
    def test_str_method(self):
        article = ArticleFactory(title="Test")
        assert str(article) == "Test"

    def test_likes_count(self):
        article = ArticleFactory()
        user1 = UserFactory()
        user2 = UserFactory()
        article.likes.add(user1, user2)
        assert article.likes_count() == 2
