import factory
from django.contrib.auth.models import User
from articles.models import Article
from companies.models import Company

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    username = factory.Sequence(lambda n: f'user{n}')
    password = factory.PostGenerationMethodCall('set_password', 'password')

class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Company
    name = factory.Sequence(lambda n: f'Company {n}')
    slug = factory.Sequence(lambda n: f'company-{n}')

class ArticleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Article
    title = factory.Sequence(lambda n: f'Article {n}')
    slug = factory.Sequence(lambda n: f'article-{n}')
    summary = factory.Faker('sentence')
    content = factory.Faker('paragraph')
    company = factory.SubFactory(CompanyFactory)
    author = factory.SubFactory(UserFactory)
