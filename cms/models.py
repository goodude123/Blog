from django.db import models
from django.contrib.auth.models import User


class Article(models.Model):
    title = models.TextField(max_length=30)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.title


class ArticleChange(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    old_title = models.TextField(max_length=30)
    new_title = models.TextField(max_length=30)
    old_content = models.TextField()
    new_content = models.TextField()
    edit_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-edit_date']

    def __str__(self):
        repr = str(self.new_title) + ' ' + str(self.edit_date)
        return repr
