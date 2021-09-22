# Generated by Django 3.2.7 on 2021-09-22 17:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0006_auto_20210922_1735'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answer',
            old_name='question_id',
            new_name='question',
        ),
        migrations.RemoveField(
            model_name='question',
            name='poll',
        ),
        migrations.RemoveField(
            model_name='question',
            name='text',
        ),
        migrations.AddField(
            model_name='question',
            name='type',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3)], default=1),
        ),
        migrations.CreateModel(
            name='Question_choice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('words', models.CharField(max_length=120)),
                ('question_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='text', to='poll.question')),
            ],
        ),
    ]
