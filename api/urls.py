from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken import views as auth_views
from . import views


router = routers.DefaultRouter()
router.register('article', views.ArticleView)

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', auth_views.obtain_auth_token, name='api-token-auth')
]
