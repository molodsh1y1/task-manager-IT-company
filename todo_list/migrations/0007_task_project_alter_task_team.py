# Generated by Django 5.1.3 on 2024-12-04 00:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_team_owner'),
        ('todo_list', '0006_alter_project_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='todo_list.project'),
        ),
        migrations.AlterField(
            model_name='task',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='accounts.team'),
        ),
    ]
