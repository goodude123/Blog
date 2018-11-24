from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from .models import Article, ArticleChange
from .decorators import prevent_logged
from .forms import ArticleForm


class Main(ListView):
    template_name = 'cms/articles_list.html'
    context_object_name = 'articles'
    model = Article
    
    def get_queryset(self):
        return self.model.objects.all()[:3]


class SingleArticle(DetailView):
    model = Article
    template_name = 'cms/article.html'

@prevent_logged
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            user = authenticate(username=username, password=password)
            login(request, user)

            return redirect(reverse('cms:main'))
        else:
            return redirect(reverse('cms:register'))
            
    elif request.method == 'GET':
        form = UserCreationForm()
        return render(request, 'registration/register.html', {'form': form})


@login_required
def add_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            author = request.user
            pub_date = timezone.now()
            article = Article(
                title=title,
                content=content,
                author=author,
                pub_date=pub_date
            )
            article.save()
            return redirect(reverse('cms:main'))
        else:
            redirect(reverse('cms:add_article'))

    elif request.method == 'GET':
        form = ArticleForm()
        return render(request, 'cms/add_article.html', {'form': form})


@login_required
def edit_article(request, id_article):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            new_title = form.cleaned_data['title']
            new_content = form.cleaned_data['content']
            
            article = get_object_or_404(Article, pk=id_article)
            old_title = article.title
            old_content = article.content

            article.title = new_title
            article.content = new_content

            change = ArticleChange(
                article=article,
                user=request.user,
                old_title=old_title,
                new_title=new_title,
                old_content=old_content,
                new_content=new_content,
            )

            article.save()
            change.save()

        return redirect(reverse('cms:article', kwargs={'pk': id_article}))

    elif request.method == 'GET':
        article = get_object_or_404(Article, pk=id_article)
        form = ArticleForm(instance=article)
        return render(request, 'cms/edit_article.html', {'form': form, 'id_article': id_article})


def delete_article(request, id_article):
    if request.user.is_superuser:
        article = get_object_or_404(Article, pk=id_article)
        article_title = article.title
        article.delete()
        information = 'Deleted article ' + article_title
        return render(request, 'cms/information.html', {'information': information, 'title': 'Deleted'})
    else:
        information = 'Denied access'
        title = 'Denied access'
        return render(request, 'cms/information.html', {'information': information, 'title': title})
