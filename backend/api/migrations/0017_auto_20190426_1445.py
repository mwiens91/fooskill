# Generated by Django 2.2 on 2019-04-26 21:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_matchupstatsnode'),
    ]

    operations = [
        migrations.CreateModel(
            name='RatingPeriod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_datetime', models.DateTimeField(help_text='The starting datetime for the rating period.')),
                ('end_datetime', models.DateTimeField(help_text='The starting datetime for the rating period.')),
            ],
            options={
                'ordering': ['-end_datetime'],
            },
        ),
        migrations.CreateModel(
            name='PlayerRatingsNode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.FloatField(help_text="The player's rating for this rating period.")),
                ('rating_deviation', models.FloatField(help_text="The player's rating deviation for this rating period.")),
                ('rating_volatility', models.FloatField(help_text="The player's rating volatility for this rating period.")),
                ('player', models.ForeignKey(help_text='The player corresponding whose ratings this node is for.', on_delete=django.db.models.deletion.CASCADE, to='api.Player')),
                ('rating_period', models.ForeignKey(help_text='The rating period this rating was calculated in', on_delete=django.db.models.deletion.CASCADE, to='api.RatingPeriod')),
            ],
            options={
                'ordering': ['-pk'],
            },
        ),
        migrations.AddField(
            model_name='game',
            name='rating_period',
            field=models.ForeignKey(blank=True, help_text='The rating period this game is apart of', null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.RatingPeriod'),
        ),
    ]
