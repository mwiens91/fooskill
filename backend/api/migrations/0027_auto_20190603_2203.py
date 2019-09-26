# Generated by Django 2.2 on 2019-06-04 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_auto_20190528_1541'),
    ]

    operations = [
        migrations.AddField(
            model_name='matchupstatsnode',
            name='average_goals_against_per_game',
            field=models.FloatField(default=0, help_text='The average number of goals scored per game by player2.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='playerstatsnode',
            name='average_goals_against_per_game',
            field=models.FloatField(default=0, help_text='The average number of goals scored against the player per game.'),
            preserve_default=False,
        ),
    ]