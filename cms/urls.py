from cms import views
from django.urls import path, include

app_name = 'cms'

urlpatterns = [
    path('', views.Main.as_view(), name='main'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.register, name='register'),
    path('article/<int:pk>', views.SingleArticle.as_view(), name='article'),
    path('add_article/', views.add_article, name='add_article'),
    path('edit_article/<int:id_article>/', views.edit_article, name='edit_article'),
    path('delete_article/<int:id_article>/', views.delete_article, name='delete_article'),
]
