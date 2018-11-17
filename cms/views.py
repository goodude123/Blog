from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.utils import timezone
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from .models import Article
from .decorators import prevent_logged
from .forms import AddArticleForm


class Main(ListView):
    template_name = 'cms/articles_list.html'
    context_object_name = 'articles'
    model = Article
    
    def get_queryset(self):
        return self.model.objects.all()[:3]


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
        form = AddArticleForm(request.POST)
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
        form = AddArticleForm()
        return render(request, 'cms/add_article.html', {'form': form})


@login_required
def edit_article(request):
    return HttpResponse
