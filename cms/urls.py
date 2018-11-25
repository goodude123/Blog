from django.urls import path, include
from cms import views


app_name = 'cms'

urlpatterns = [
    path('', views.Main.as_view(), name='main'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.register, name='register'),
    path('article/<int:pk>/', views.SingleArticle.as_view(), name='article'),
    path('article/add/', views.add_article, name='add_article'),
    path('article/edit/<int:id_article>/', views.edit_article, name='edit_article'),
    path('article/delete/<int:id_article>/', views.delete_article, name='delete_article'),
]
