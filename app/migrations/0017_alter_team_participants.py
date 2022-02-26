# Generated by Django 4.0.2 on 2022-02-26 20:40

import app.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_remove_membership_team_membership_a'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='participants',
            field=models.ManyToManyField(default=app.models.CustomUser, related_name='participa', to=settings.AUTH_USER_MODEL),
        ),
    ]
