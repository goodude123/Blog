from django.urls import path, include
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register('article', views.ArticleView)

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', views.ObtainAuthTokenAndUserId.as_view(), name='api-token-auth')
]
