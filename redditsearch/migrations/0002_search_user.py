# Generated by Django 2.1.3 on 2018-11-20 04:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('redditsearch', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='search',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='searches', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]