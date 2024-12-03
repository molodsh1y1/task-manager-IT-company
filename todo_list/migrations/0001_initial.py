# Generated by Django 5.1.3 on 2024-12-01 17:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('NOT_STARTED', 'Not Started'), ('IN_PROGRESS', 'In Progress'), ('COMPLETED', 'Completed'), ('BLOCKED', 'Blocked')], default='IN_PROGRESS', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('deadline', models.DateTimeField(blank=True, null=True)),
                ('is_completed', models.BooleanField()),
                ('priority', models.CharField(choices=[('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High')], default='LOW', max_length=20)),
                ('task_type', models.CharField(choices=[('BUG', 'Bug'), ('NEW_FEATURE', 'New Feature'), ('BREAKING_CHANGE', 'Breaking Change'), ('REFACTORING', 'Refactoring'), ('QA', 'Quality Assurance')], default='NEW_FEATURE', max_length=20)),
                ('status', models.CharField(choices=[('NOT_STARTED', 'Not Started'), ('IN_PROGRESS', 'In Progress'), ('COMPLETED', 'Completed'), ('BLOCKED', 'Blocked')], default='IN_PROGRESS', max_length=20)),
                ('assignees', models.ManyToManyField(related_name='tasks', to=settings.AUTH_USER_MODEL)),
                ('tags', models.ManyToManyField(blank=True, related_name='tasks', to='todo_list.tag')),
                ('team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tasks', to='accounts.team')),
            ],
        ),
    ]