import pytest
from django.urls import reverse
from articles.models import Article
from ..factories import ArticleFactory, UserFactory, CompanyFactory

@pytest.mark.django_db
def test_article_list_view(client):
    ArticleFactory.create_batch(15)
    url = reverse('articles:article-list')
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.context['articles']) == 10

@pytest.mark.django_db
def test_article_list_htmx_pagination(client):
    ArticleFactory.create_batch(25)
    url = reverse('articles:article-list') + '?page=2'
    response = client.get(url, HTTP_HX_REQUEST='true')
    assert response.status_code == 200
    # Проверим, что вернулся фрагмент (можно по шаблону или содержимому)
    assert 'article-card' in response.content.decode()
    # Должен быть именно фрагмент, без обертки страницы
    assert '<h1>Новости IT</h1>' not in response.content.decode()

@pytest.mark.django_db
def test_like_article(client):
    user = UserFactory()
    article = ArticleFactory()
    client.force_login(user)
    url = reverse('articles:like-article', args=[article.pk])
    response = client.post(url, HTTP_HX_REQUEST='true')
    assert response.status_code == 200
    assert article.likes.filter(id=user.id).exists()
    # Проверим, что вернулась кнопка с обновленным счетчиком
    assert 'Лайк (1)' in response.content.decode()
