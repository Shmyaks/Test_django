# Generated by Django 3.2.7 on 2021-09-23 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0010_alter_answer_ans'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='question',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
