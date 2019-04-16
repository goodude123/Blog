from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, Http404
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, FormView, DeleteView, TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from .models import Article, ArticleChange
from .decorators import prevent_logged, prevent_logged_class_view
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


@method_decorator(prevent_logged_class_view, name='dispatch')
class RegisterView(FormView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return redirect(reverse('cms:main'))

    def form_invalid(self, form):
        return redirect(reverse('cms:register'))


@method_decorator(login_required, name='dispatch')
class AddArticleView(FormView):
    form_class = ArticleForm
    template_name = 'cms/add_article.html'

    def form_valid(self, form):
        self.create_article(form)
        return redirect(reverse('cms:main'))
    
    def create_article(self, form):
        title = form.cleaned_data['title']
        content = form.cleaned_data['content']
        author = User.objects.get(pk=self.request.user.pk)
        pub_date = timezone.now()
        article = Article(
            title=title,
            content=content,
            author=author,
            pub_date=pub_date
        )
        article.save()

    def form_invalid(self, form):
        redirect(reverse('cms:add_article'))


class EditArticleView(FormView):
    form_class = ArticleForm
    template_name = 'cms/edit_article.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = get_object_or_404(Article, pk=self.kwargs['id_article'])
        form = self.form_class(instance=instance)
        context['form'] = form
        context['id_article'] = self.kwargs['id_article']
        return context

    def form_valid(self, form):
        new_title = form.cleaned_data['title']
        new_content = form.cleaned_data['content']
        
        article = get_object_or_404(Article, pk=self.kwargs['id_article'])
        old_title = article.title
        old_content = article.content

        article.title = new_title
        article.content = new_content

        change = ArticleChange(
            article=article,
            user=self.request.user,
            old_title=old_title,
            new_title=new_title,
            old_content=old_content,
            new_content=new_content,
        )

        article.save()
        change.save()
        return redirect(reverse('cms:article', kwargs={'pk': self.kwargs['id_article']}))

    def form_invalid(self, form):
        return redirect(reverse('cms:article', kwargs={'pk': self.kwargs['id_article']}))


class DeleteArticleView(DeleteView):
    model = Article
    queryset = None
    success_url = reverse_lazy('cms:delete_article_success')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        if request.user.is_superuser or (request.user == self.object.author):
            return super().delete(request, *args, **kwargs)
        return self.redirect_denied_access()

    def redirect_denied_access(self):
        return redirect(reverse_lazy('cms:denied_access'))


class DeniedAccessView(TemplateView):
    template_name = 'cms/denied_access.html'


class DeleteArticleSuccessView(TemplateView):
    template_name = 'cms/delete_article_success.html'
