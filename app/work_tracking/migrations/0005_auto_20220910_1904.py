# Generated by Django 3.2 on 2022-09-10 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work_tracking', '0004_rename_achievment_worktimelog_achievement'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='leader',
        ),
        migrations.AddField(
            model_name='employee',
            name='is_leader',
            field=models.BooleanField(default=False),
        ),
    ]
