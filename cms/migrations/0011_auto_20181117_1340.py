# Generated by Django 2.1.3 on 2018-11-17 13:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0010_auto_20181117_1336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='edit_history',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cms.ArticleChanges'),
        ),
    ]
