# Generated by Django 4.0.2 on 2022-02-27 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0024_remove_goal_team_goal_team'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='team',
            field=models.ManyToManyField(related_name='gooals', to='app.Team'),
        ),
    ]