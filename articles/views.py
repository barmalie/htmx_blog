from django.views.generic import ListView, DetailView
from .models import Article
from .mixins import HtmxTemplateMixin

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string

class ArticleListView(HtmxTemplateMixin, ListView):
    model = Article
    template_name = 'articles/article_list.html'
    htmx_template_name = 'includes/article_cards.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        # фильтрация по компании, если передан параметр
        company_id = self.request.GET.get('company')
        if company_id:
            queryset = queryset.filter(company_id=company_id)
        return queryset.select_related('company', 'author')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['companies'] = Company.objects.all()
        return context

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'articles/article_detail.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.select_related('author').all()
        return context



@login_required
def like_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.user in article.likes.all():
        article.likes.remove(request.user)
    else:
        article.likes.add(request.user)
    # Возвращаем обновленную кнопку
    html = render_to_string('includes/like_button.html', {'article': article})
    return HttpResponse(html)
