# Generated by Django 5.1.3 on 2024-12-04 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_list', '0005_remove_task_projects_project_team'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
