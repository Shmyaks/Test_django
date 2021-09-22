# Generated by Django 3.2.7 on 2021-09-21 21:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('poll', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to=settings.AUTH_USER_MODEL),
        ),
    ]
