# Generated by Django 2.2 on 2019-04-26 01:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_auto_20190425_1744'),
    ]

    operations = [
        migrations.CreateModel(
            name='MatchupStatsNode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('games', models.PositiveIntegerField(help_text='The number of games played by the matchup.')),
                ('wins', models.PositiveIntegerField(help_text='The number of wins the player1 has.')),
                ('losses', models.PositiveIntegerField(help_text='The number of losses the player1 has.')),
                ('average_goals_per_game', models.FloatField(help_text='The average number of goals scored per game by player1.')),
                ('game', models.ForeignKey(help_text="The latest game which updated the matchup's stats.", on_delete=django.db.models.deletion.CASCADE, to='api.Game')),
                ('player1', models.ForeignKey(help_text='The player in the matchup whose perspective to take.', on_delete=django.db.models.deletion.CASCADE, related_name='player1', to='api.Player')),
                ('player2', models.ForeignKey(help_text='The "opponent" player in the matchup.', on_delete=django.db.models.deletion.CASCADE, related_name='player2', to='api.Player')),
            ],
            options={
                'ordering': ['-pk'],
            },
        ),
    ]
