from cms import views
from django.urls import path, include

app_name = 'cms'

urlpatterns = [
    path('', views.Main.as_view(), name='main'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.register, name='register'),
    path('add_article/', views.add_article, name='add_article')
]
