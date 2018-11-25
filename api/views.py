from django.shortcuts import render
from rest_framework import viewsets
from cms.models import Article
from .serializers import ArticleSerializer


class ArticleView(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
