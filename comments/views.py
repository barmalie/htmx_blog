from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from articles.models import Article
from .models import Comment
from .forms import CommentForm

@login_required
def add_comment(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.author = request.user
            comment.save()
            # Возвращаем HTML одного комментария
            html = render_to_string('includes/comment_item.html', {'comment': comment})
            return HttpResponse(html)
        else:
            # В случае ошибки возвращаем форму с ошибками
            html = render_to_string('includes/comment_form.html', {'form': form, 'article': article})
            return HttpResponse(html, status=400)
    return HttpResponse(status=405)  # Метод не разрешён

