from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from .models import Post


class Main(ListView):
    template_name = 'post_list.html'
    context_object_name = 'posts'
    model = Post
    
    def get_queryset(self):
        return self.model.objects.all()[:3]


def register(request):
    if request.method == 'POST':
        return HttpResponse
    elif request.method == 'GET':
        return render(request, 'registration/registration.html')


@login_required
def add_post(request):
    return HttpResponse


@login_required
def edit_post(request):
    return HttpResponse
