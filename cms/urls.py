from django.urls import path, include
from cms import views


app_name = 'cms'

urlpatterns = [
    path('', views.Main.as_view(), name='main'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.RegisterView.as_view(), name='register'),
    path('article/<int:pk>/', views.SingleArticle.as_view(), name='article'),
    path('article/add/', views.AddArticleView.as_view(), name='add_article'),
    path('article/edit/<int:id_article>/', views.EditArticleView.as_view(), name='edit_article'),
    path('article/delete/<int:pk>/', views.DeleteArticleView.as_view(), name='delete_article'),
    path('article/delete/success/', views.DeleteArticleSuccessView.as_view(), name='delete_article_success'),
    path('denied/', views.DeniedAccessView.as_view(), name='denied_access'),
]
